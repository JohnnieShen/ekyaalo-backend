from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.usability import add_usability
from schemas import UsabilityEntry

blp = Blueprint("usability", __name__, description="Operations for usability study")

@blp.route("/usability")
class Usability(MethodView):
  @blp.arguments(UsabilityEntry)
  @blp.response(201, UsabilityEntry)
  def post(self, new_data):
    result = add_usability(new_data)
    if not result:
      abort(400, message = "Failed to post usability entry.")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response