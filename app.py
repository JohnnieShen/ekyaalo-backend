from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from resources.patient import blp as PatientBlueprint
from resources.submission import blp as SubmissionBlueprint
from resources.operator import blp as OperatorBlueprint
from resources.pathologist import blp as PathologistBlueprint
from resources.hc import blp as HealthCenterBlueprint
from resources.gp import blp as GPBlueprint



# from flask_uploads import UploadSet, configure_uploads, IMAGES
# from resources.image_resources import ImageUploadResource

app = Flask(__name__)

CORS(app)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "GymConnect API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(PatientBlueprint)
api.register_blueprint(SubmissionBlueprint)
api.register_blueprint(OperatorBlueprint)
api.register_blueprint(PathologistBlueprint)
api.register_blueprint(HealthCenterBlueprint)
api.register_blueprint(GPBlueprint)

# Configure Flask-Uploads
# photos = UploadSet('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'path/to/uploaded/images'
# configure_uploads(app, photos)


