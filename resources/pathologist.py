from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.pathologist import add_path, get_pathologists, get_pathologist_by_id, patho_update_submission
from schemas import PathologistSchema, PathoSubmissionUpdateSchema

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

@blp.route("/pathologist/submission/update")
class Pathologist(MethodView):
  @blp.arguments(PathoSubmissionUpdateSchema)
  def put(self, new_data):
    result = patho_update_submission(new_data)
    if not result:
      abort(400, message = "Failed to update submission. Pathologist or submission may not exist.")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

