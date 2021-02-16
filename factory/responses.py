from typing import Dict, Any

from flask import jsonify

from constants import codes, keys, messages


class ResponseFactory:
    def __init__(self, obj_name: str):
        self._obj_name = obj_name

    def error_inserting(self, json=False):
        return self._message_response(messages.ERROR_INSERTING.format(self._obj_name),
                                      codes.INTERNAL_ERROR, json=json)

    def error_already_exists(self, attr_name: str, json=False):
        return self._message_response(messages.ERROR_ALREADY_EXISTS.format(self._obj_name, attr_name),
                                      codes.BAD_REQUEST, json=json)

    def error_not_found(self, json=False):
        return self._message_response(messages.ERROR_NOT_FOUND.format(self._obj_name), codes.NOT_FOUND, json)

    def ok_deleted(self, plural=False, json=False):
        plural_suffix = "s" if plural else ""
        return self._message_response(messages.OK_DELETED.format(plural_suffix, self._obj_name), codes.OK, json)

    @classmethod
    def ok_created(cls, payload: Dict[str, Any], json=False):
        return cls._payload_response(payload, codes.ACCEPTED, json)

    @classmethod
    def _payload_response(cls, payload: Dict[str, Any], code: int, json):
        return jsonify(payload) if json else payload, code

    @classmethod
    def _message_response(cls, message: str, code: int, json: bool):
        payload = {keys.MESSAGE: message}
        return cls._payload_response(payload, code, json)
