from flask import request


def get_request_data():
    if request.is_json:
        return request.get_json()
    return {key: value for key, value in request.form.items()}
