from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from resources.patient import blp as PatientBlueprint
from resources.submission import blp as SubmissionBlueprint
from resources.operator import blp as OperatorBlueprint
from resources.pathologist import blp as PathologistBlueprint
from resources.hc import blp as HealthCenterBlueprint
from resources.gp import blp as GPBlueprint
from resources.collection import blp as CollectionBlueprint
from resources.usability import blp as UsabilityBlueprint

app = Flask(__name__)
app.config['TIMEOUT'] = 120
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
api.register_blueprint(CollectionBlueprint)
api.register_blueprint(UsabilityBlueprint)