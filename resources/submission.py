from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask import make_response

from databases.submission import get_submissions, get_submission, get_oper_submission, add_submission, upload_image, fill_submission, retrieve_images
from schemas import SubmissionSchema, SubmissionFormSchema, ImageUploadSchema, ImageRetrieveSchema

blp = Blueprint("submissions", __name__, description="Operations on submissions")

@blp.route("/submission")
class Submission(MethodView):
  @blp.response(200, SubmissionSchema(many=True))
  def get(self):
    result = get_submissions()
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
  @blp.arguments(SubmissionSchema)
  @blp.response(201, SubmissionSchema)
  def post(self, new_data):
    result = add_submission(new_data)
    if not result:
      abort(400, message = "Failed to add submission")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/submission/operator/<int:id>")
class Submission(MethodView):
  @blp.response(200, SubmissionSchema(many=True))
  def get(self, id):
    result = get_oper_submission(id)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@blp.route("/submission/<int:id>")
class Submission(MethodView):
  @blp.response(200, SubmissionSchema)
  def get(self, id):
    result = get_submission(id)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/submission/upload")
class Submission(MethodView):
  @blp.arguments(SubmissionFormSchema)
  @blp.response(200, SubmissionFormSchema)
  def post(self, new_data):
    result = fill_submission(new_data)
    if not result:
      abort(400, message = "Failed to fill submission. Submission likely already exists for this patient on this day.")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
  
@blp.route("/submission/upload/image")
class Submission(MethodView):
  @blp.arguments(ImageUploadSchema)
  def post(self, data):
    result = upload_image(data)
    if result == "Submission does not exist":
      abort(400, message = "Submission does not exist")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@blp.route("/submission/upload/image/<int:id>")
class Submission(MethodView):
  def get(self, id):
    result = retrieve_images(id)
    if result == "Submission does not exist":
      abort(400, message = "Submission does not exist")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response