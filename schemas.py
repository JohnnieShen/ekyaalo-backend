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