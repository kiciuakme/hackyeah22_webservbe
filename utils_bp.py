from flask import Blueprint, send_from_directory

utils_bp = Blueprint("utils",__name__,url_prefix='/utils')

@utils_bp.route("hello_world", methods=["GET"])
def hello_world():
    """
        Returns "hello world" string
    """
    return "hello world"

@utils_bp.route("favicon", methods=["GET"])
def favicon():
    return send_from_directory('', 'favicon.ico', mimetype='image/vnd.microsoft.icon')