def check_add_category_request(data):
    if "category_name" not in data or "max_field" not in data:
        return False
    return True


def check_add_field_request(data):
    if "category_name" not in data or "field_name" not in data or "image" not in data:
        return False
    return True
