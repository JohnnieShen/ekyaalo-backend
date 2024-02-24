from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.operator import add_operator, get_operators, get_operator_by_id
from schemas import OperatorSchema

blp = Blueprint("operators", __name__, description="Operations on operators")

@blp.route("/operator")
class Submission(MethodView):
  @blp.arguments(OperatorSchema)
  @blp.response(201, OperatorSchema)
  def post(self, new_data):
    result = add_operator(new_data)
    if not result:
      abort(400, message = "Operator already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

  @blp.response(200, OperatorSchema(many=True))
  def get(self):
    result = get_operators()
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/operator/<int:operator_id>")
class OperatorById(MethodView):
  @blp.response(200, OperatorSchema)
  def get(self, operator_id):
    result = get_operator_by_id(operator_id)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  