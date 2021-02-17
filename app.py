"""This is a simple API"""

import os
from http import HTTPStatus

from flask import Flask, request
from flask_redis import FlaskRedis
from werkzeug.exceptions import HTTPException

APP = Flask(__name__)
APP.config["REDIS_URL"] = "redis://%s:6379/0" % os.getenv("REDIS_HOST", "localhost")
REDIS_CLIENT = FlaskRedis(APP)


@APP.route("/")
def hello():
    """Simple endpoint for /"""
    return "Hello, App!"


@APP.route("/version")
def version():
    """Simple endpoint for /version"""
    return os.getenv("APP_VERSION", "No version")


@APP.route("/messages/<message>", methods=["GET"])
def get_message(message):
    """GET messages handler"""
    msg = REDIS_CLIENT.get(message)
    if msg is None:
        return "Not Found", HTTPStatus.NOT_FOUND
    return msg.decode("utf-8")


@APP.route("/messages/<message>", methods=["PUT"])
def put_message(message):
    """PUT messages handler"""
    if request.headers["Content-Type"] != "application/json":
        return (
            "HTTP header 'Content-Type: application/json' expected",
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        )
    REDIS_CLIENT.set(message, request.json)
    return "Created", HTTPStatus.CREATED


@APP.route("/messages/<message>", methods=["DELETE"])
def delete_message(message):
    """DELETE messages handler"""
    if REDIS_CLIENT.delete(message) == 1:
        return "Deleted", HTTPStatus.NO_CONTENT
    return "Not Found", HTTPStatus.NOT_FOUND


@APP.errorhandler(HTTPException)
def handle_http_exception(exception: HTTPException):
    """Handler for HTTPException"""
    return (exception.description, exception.code)


@APP.errorhandler(Exception)
def handle_exception():
    """Handler for generic Exception"""
    return (
        HTTPStatus.INTERNAL_SERVER_ERROR.description,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
