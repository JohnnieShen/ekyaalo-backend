from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.operator import add_operator, get_operators, get_operator_by_id, login_operator
from schemas import OperatorSchema, OperatorLoginSchema

blp = Blueprint("operators", __name__, description="Operations on operators")

@blp.route("/operator")
class Operator(MethodView):
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
class Operator(MethodView):
  @blp.response(200, OperatorSchema)
  def get(self, operator_id):
    result = get_operator_by_id(operator_id)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@blp.route("/operator/login")
class Operator(MethodView):
  @blp.arguments(OperatorLoginSchema)
  @blp.response(200, OperatorSchema)
  def get(self, new_data):
    result = login_operator(new_data["fname"], new_data["lname"], new_data["hc_name"])
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
