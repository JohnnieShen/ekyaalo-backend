from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask import make_response

from databases.submission import get_submissions, get_submission, add_submission, upload_image, fill_submission
from schemas import SubmissionSchema, SubmissionFormSchema, ImageUploadSchema

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
  
@blp.route("/submission/<int:id>")
class Submission(MethodView):
  @blp.response(200, SubmissionSchema(many=True))
  def get(self, id):
    result = get_submission(id)
    # upload_image(None)
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
  

# photos = UploadSet('photos', IMAGES)

@blp.route("/submission/upload/image")
class Submission(MethodView):
  # @blp.response(200, SubmissionFormSchema)
  def post(self):
        # try:
        #     photo = request.files['photo']
        #     filename = photos.save(photo)
        #     # Store the filename or URL in your database or Supabase storage
        #     # ...

        #     return jsonify({"message": "Image uploaded successfully"})
        # except Exception as e:
        #     return jsonify({"error": str(e)}), 400
    data = request.json
    result = upload_image(data)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response