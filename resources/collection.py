from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import make_response
from databases.collection import upload_case
from schemas import CollectionSchema

blp = Blueprint("data collection", __name__, description="Operations on data collection")

@blp.route("/datacollection")
class DataCollection(MethodView):
  @blp.arguments(CollectionSchema)
  @blp.response(200, CollectionSchema)
  def post(self, new_data):
    result = upload_case(new_data)
    if not result:
      abort(404, message="Failed to upload case")
    response = make_response(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response