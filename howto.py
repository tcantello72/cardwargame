"""
created by: Toby Cantello
Date created: 8/22/23
Last updated: 8/22/23
""" 

from flask import Blueprint, render_template

howto_blueprint = Blueprint("howto_blueprint", __name__, static_folder="static", template_folder="templates")

@howto_blueprint.route("/howto", methods=["POST", "GET"])
def howto():
    return render_template("howto.html")