from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.pathologist import add_path, get_pathologists, get_pathologist_by_id, patho_update_submission, get_path_submissions, login_patho
from schemas import PathologistSchema, PathoSubmissionUpdateSchema, PathoLoginSchema

blp = Blueprint("pathologists", __name__, description="Operations on pathologists")

@blp.route("/pathologist")
class Pathologist(MethodView):
  @blp.arguments(PathologistSchema)
  @blp.response(201, PathologistSchema)
  def post(self, new_data):
    result = add_path(new_data)
    if not result:
      abort(400, message = "Pathologist already exists")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

  @blp.response(200, PathologistSchema(many=True))
  def get(self):
    result = get_pathologists()
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/pathologist/<int:path_id>")
class PathologistById(MethodView):
  @blp.response(200, PathologistSchema)
  def get(self, path_id):
    result = get_pathologist_by_id(path_id)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@blp.route("/pathologist/submission")
class Pathologist(MethodView):
  @blp.arguments(PathoSubmissionUpdateSchema)
  def put(self, new_data):
    result = patho_update_submission(new_data)
    if not result:
      abort(400, message = "Failed to update submission. Pathologist or submission may not exist.")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@blp.route("/pathologist/submission/<int:path_id>")
class Pathologist(MethodView):
  def get(self, path_id):
    result = get_path_submissions(path_id)
    if type(result) == str:
      abort(400, message = result)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/pathologist/login")
class Pathologist(MethodView):
  @blp.arguments(PathoLoginSchema)
  @blp.response(200, PathologistSchema)
  def post(self, new_data):
    result = login_patho(new_data["fname"], new_data["lname"])
    if not result:
      abort(400, message = "Failed to login pathologist. The pathologist may not exist.")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    


