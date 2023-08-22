"""
created by: Toby Cantello
Date created: 8/21/23
Last updated: 8/21/23
""" 

from flask import Blueprint, render_template

creator_blueprint = Blueprint("creator_blueprint", __name__, static_folder="static", template_folder="templates")

@creator_blueprint.route("/creator", methods=["POST", "GET"])
def creator():
    return render_template("creator.html")