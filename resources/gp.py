from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.gp import add_gp, get_gp, get_gp_by_id
from schemas import GPSchema

blp = Blueprint("general practitioners", __name__, description="Operations on general practitioners")

@blp.route("/gp")
class Submission(MethodView):
  @blp.arguments(GPSchema)
  @blp.response(201, GPSchema)
  def post(self, new_data):
    result = add_gp(new_data)
    if not result:
      abort(400, message = "General Practitioner already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

  @blp.response(200, GPSchema(many=True))
  def get(self):
    result = get_gp()
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/gp/<int:gp_id>")
class GPById(MethodView):
  @blp.response(200, GPSchema)
  def get(self, gp_id):
    result = get_gp_by_id(gp_id)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response