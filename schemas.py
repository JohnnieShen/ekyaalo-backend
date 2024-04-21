from marshmallow import Schema, fields

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)
    sex = fields.Str(required=True)
    birthdate = fields.Str(required=True)
    village = fields.Str(required=True)
    email = fields.Str()
    phone_number = fields.Str()
    kin_name = fields.Str()
    kin_relation = fields.Str()
    tribe = fields.Str()
    race = fields.Str()

class SubmissionSchema(Schema):
    sub_id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    operator_id = fields.Int(required=True)
    date_biopsy = fields.Str(required=True)
    hc_id = fields.Int(required=True)
    clinical_workup = fields.Str()
    req_phys_id = fields.Int(required=True)
    stain = fields.Str()
    specimen = fields.Str()
    op_dx = fields.Str()
    microscopic = fields.Str()
    path_dx = fields.Str()
    path_id = fields.Int()
    signed_date = fields.Str()
    image_list = fields.List(fields.List(fields.Str()))

class OperatorSchema(Schema):
    id = fields.Int(dump_only=True)
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)

class OperatorLoginSchema(Schema):
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)
    hc_name = fields.Str(required=True)

class PathologistSchema(Schema):
    id = fields.Int(dump_only=True)
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)
    email = fields.Str()
    phone_number = fields.Str()
    health_centers = fields.List(fields.Int())

class PathoLoginSchema(Schema):
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)

class HealthCenterSchema(Schema):
    name = fields.Str(required=True)
    county = fields.Str(required=True)

class GPSchema(Schema):
    id = fields.Int(dump_only=True)
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)
    email = fields.Str()
    phone_number = fields.Str()

# data collection workflow
class CollectionImageSchema(Schema):
    mag1 = fields.String(required=True) # first magnification, image as byte string
    mag2 = fields.String() # second magnification, image as byte string
    type = fields.String()

class CollectionSlideSchema(Schema):
    slidename = fields.String(required=True)
    imagelist = fields.List(fields.Nested(CollectionImageSchema()), required=True)

class CollectionSchema(Schema):
    case_id = fields.String(required=True)
    slides = fields.List(fields.Nested(CollectionSlideSchema()), required=True)

# normal workflow
class ImageSchema(Schema):
    image = fields.Str(required=True)
    type = fields.Str(required=True)

class SlideSchema(Schema):
    slidename = fields.Str(required=True)
    imagelist = fields.List(fields.Nested(ImageSchema()), required=True)

class SubmissionFormSchema(Schema):
    # explicit form fields
    patient_fname = fields.Str(required=True)
    patient_lname = fields.Str(required=True)
    patient_sex = fields.Str(required=True)
    patient_birthdate = fields.Str(required=True)
    patient_village = fields.Str(required=True)
    patient_email = fields.Str()
    patient_phone_number = fields.Str()
    kin_name = fields.Str()
    kin_relation = fields.Str()
    tribe = fields.Str()
    race = fields.Str()
    clinical_workup = fields.Str()
    stain = fields.Str()
    req_phys_fname = fields.Str(required=True)
    req_phys_lname = fields.Str(required=True)
    date = fields.Str(required=True)
    specimen = fields.Str(required=True)

    # implicit from state, ML model
    operator_id = fields.Int(required=True)
    hc_id = fields.Int(required=True)
    operator_dx = fields.Str(required=True)

    # image list
    images = fields.List(fields.Nested(SlideSchema()), required=True)

class PathoSubmissionUpdateSchema(Schema):
    sub_id = fields.Int(required=True)
    path_dx = fields.Str(required=True)
    path_id = fields.Int(required=True)
    signed_date = fields.Str(required=True)

class PathoLoginSchema(Schema):
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)

class UsabilityEntry(Schema):
    captureImage = fields.List(fields.Str())
    determineAdequacy = fields.List(fields.Str())
    enterPatientInfo = fields.List(fields.Str())
    login = fields.List(fields.Str())
    navigateClusters = fields.List(fields.Str())
    provideAction = fields.List(fields.Str())
    reviewRecords = fields.List(fields.Str())
    selectCluster = fields.List(fields.Str())
    setupAndCalibration = fields.List(fields.Str())
    stopCapture = fields.List(fields.Str())
    syncToInternet = fields.List(fields.Str())
    tutorial = fields.List(fields.Str())
