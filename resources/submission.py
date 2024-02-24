from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.submission import get_submissions, get_submission, add_submission
from schemas import SubmissionSchema

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
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response