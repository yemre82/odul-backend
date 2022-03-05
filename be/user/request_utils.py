def check_register_request(data):
    if "device_id" not in data:
        return False
    return True