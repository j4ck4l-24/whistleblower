def extract_nested_value(response_body, structure, placeholder):
    """
    Extract a nested value from a response body based on a given structure and placeholder.

    Args:
        response_body (Dict[str, Any]): The response body to extract the value from.
        structure (Dict[str, Any]): The structure defining where to find the value.
        placeholder (Any): The placeholder used in the structure to mark the desired value.

    Returns:
        Any: The extracted value, or None if not found.
    """
    def extract_path_to_placeholder(data, structure, placeholder, path=None):
        if path is None:
            path = []

        if isinstance(data, dict) and isinstance(structure, dict):
            for key in structure:
                if structure[key] == placeholder:
                    if key in data:
                        return path + [key]
                elif isinstance(structure[key], (dict, list)):
                    if key in data:
                        result = extract_path_to_placeholder(
                            data[key], structure[key], placeholder, path + [key]
                        )
                        if result:
                            return result
        elif isinstance(data, list) and isinstance(structure, list):
            for index, item in enumerate(structure):
                result = extract_path_to_placeholder(
                    data[index], item, placeholder, path + [index]
                )
                if result:
                    return result
        return None

    def get_value_from_path(data, path):
        try:
            for part in path:
                if isinstance(data, list):
                    part = int(part)  # Convert index to integer if part is a list index
                data = data.get(part, None) if isinstance(data, dict) else (data[part] if part < len(data) else None)
                if data is None:
                    return None
            return data
        except (IndexError, KeyError, TypeError):
            return None

    # Find the path to the placeholder in the structure
    path_to_placeholder = extract_path_to_placeholder(response_body, structure, placeholder)

    if path_to_placeholder is None:
        return None

    # Extract the actual value from the response body using the path
    return get_value_from_path(response_body, path_to_placeholder)

def replace_nested_value(data, placeholder, new_value):
    """
    Replace a placeholder value in a nested dictionary or list structure.

    Args:
        data (Union[Dict[str, Any], List[Any]]): The data structure to modify.
        placeholder (Any): The placeholder value to replace.
        new_value (Any): The new value to insert.

    Returns:
        Union[Dict[str, Any], List[Any]]: The modified data structure.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if value == placeholder:
                data[key] = new_value
            elif isinstance(value, (dict, list)):
                data[key] = replace_nested_value(value, placeholder, new_value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if item == placeholder:
                data[i] = new_value
            elif isinstance(item, (dict, list)):
                data[i] = replace_nested_value(item, placeholder, new_value)
    return data
