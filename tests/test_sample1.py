from flask import request
from app import APP

def test_version():
    with APP.test_request_context('/version', method='GET'):
        assert request.path == '/version'
        assert request.method == 'GET'
