"""
created by: Toby Cantello
Date created: 8/22/23
Last updated: 8/22/23
""" 

import flask
from flask import render_template

error_blueprint = flask.Blueprint("error_blueprint", __name__, static_folder="static", template_folder="templates")

@error_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')