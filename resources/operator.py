from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.operator import add_operator
from schemas import OperatorSchema

blp = Blueprint("operators", __name__, description="Operations on operators")

@blp.route("/operator")
class Submission(MethodView):
  @blp.arguments(OperatorSchema)
  @blp.response(201, OperatorSchema)
  def post(self, new_data):
    result = add_operator(new_data)
    if not result:
      abort(400, message = "Patient already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response