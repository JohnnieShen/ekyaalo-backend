from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.pathologist import add_path
from schemas import PathologistSchema

blp = Blueprint("pathologists", __name__, description="Operations on pathologists")

@blp.route("/pathologist")
class Submission(MethodView):
  @blp.arguments(PathologistSchema)
  @blp.response(201, PathologistSchema)
  def post(self, new_data):
    result = add_path(new_data)
    if not result:
      abort(400, message = "Pathologist already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response