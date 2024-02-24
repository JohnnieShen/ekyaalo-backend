from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.submission import get_submissions, get_submission
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
  

@blp.route("/submission/<string:fname>/<string:lname>")
class Submission(MethodView):
  @blp.response(200, SubmissionSchema(many=True))
  def get(self, fname, lname):
    result = get_submission(fname,lname)
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response