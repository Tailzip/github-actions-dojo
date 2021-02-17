from app import APP
from flask import request


def test_version():
    with APP.test_request_context("/version", method="GET"):
        assert request.path == "/version"
        assert request.method == "GET"
