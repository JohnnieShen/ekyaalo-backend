from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.hc import add_hc
from schemas import HealthCenterSchema

blp = Blueprint("health centers", __name__, description="Operations on health centers")

@blp.route("/hc")
class Submission(MethodView):
  @blp.arguments(HealthCenterSchema)
  @blp.response(201, HealthCenterSchema)
  def post(self, new_data):
    result = add_hc(new_data)
    if not result:
      abort(400, message = "Health Center already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response