import os
from flask import Blueprint, send_from_directory, current_app

bp = Blueprint(
    "client",
    __name__,
)

# does have a method — Flask defaults to GET.
@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, "index.html")

# send_from_directory() is a Flask helper for sending a file from a particular directory to the browser.