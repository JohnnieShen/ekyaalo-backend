from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.patient import add_patient, get_patient, get_patients
from schemas import PatientSchema

blp = Blueprint("patients", __name__, description="Operations on patients")

@blp.route("/patient")
class Patient(MethodView):
  @blp.arguments(PatientSchema)
  @blp.response(201, PatientSchema)
  def post(self, new_data):
    result = add_patient(new_data)
    if not result:
      abort(400, message = "Username already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

  @blp.response(200, PatientSchema(many=True))
  def get(self):
    result = get_patients()
    if not result:
      abort(404, message = "No patients found")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@blp.route("/patient/<int:id>")
class Patient(MethodView):
  @blp.response(200, PatientSchema)
  def get(self, id):
    result = get_patient(id)
    if not result:
      abort(404, message = "Patient not found")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

