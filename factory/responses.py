from typing import Dict, Any

from flask import jsonify

from constants import codes, keys, messages


def _payload_response(payload: Dict[str, Any], code: int, json):
    return jsonify(payload) if json else payload, code


def _message_response(message: str, code: int, json: bool):
    payload = {keys.MESSAGE: message}
    return _payload_response(payload, code, json)


def error_inserting(obj_name: str, json=False):
    return _message_response(messages.ERROR_INSERTING.format(obj_name),
                             codes.INTERNAL_ERROR, json=json)


def error_already_exists(obj_name: str, attr_name: str, json=False):
    return _message_response(messages.ERROR_ALREADY_EXISTS.format(obj_name, attr_name),
                             codes.BAD_REQUEST, json=json)


def error_not_found(obj_name: str, json=False):
    return _message_response(messages.ERROR_NOT_FOUND.format(obj_name), codes.NOT_FOUND, json)


def ok_created(payload: Dict[str, Any], json=False):
    return _payload_response(payload, codes.ACCEPTED, json)


def ok_deleted(obj_name: str, plural=False, json=False):
    plural_suffix = "s" if plural else ""
    return _message_response(messages.OK_DELETED.format(plural_suffix, obj_name), codes.OK, json)
