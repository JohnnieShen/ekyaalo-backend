import os
from supabase import create_client, Client
from PIL import Image
import base64
from io import BytesIO
import uuid

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_submission(data):
  try:
    data = supabase.table("Submission").insert(data).execute()
    return data.data
  except:
    return []

def get_submissions():
  try:
    data = supabase.table("Submission").select("*").execute()
    return data.data
  except:
    return []

# get the submissions taken by a specific operator
def get_submission(id):
  try:
    data = supabase.table("Submission").select("*").eq('operator_id', id).execute()
    return data.data
  except:
    return []
  
def fill_submission(new_data):
  # use to check if there is a patient with the same name, sex, birthdate
  patient_fname = new_data['patient_fname']
  patient_lname = new_data['patient_lname']
  patient_sex = new_data['patient_sex']
  patient_birthdate = new_data['patient_birthdate']
  data = supabase.table("Patient").select("*").eq('fname', patient_fname).eq('lname', patient_lname).eq('sex', patient_sex).eq('birthdate', patient_birthdate).execute()
  new_patient = {
      "fname": patient_fname,
      "lname": patient_lname,
      "sex": patient_sex,
      "birthdate": patient_birthdate,
      "village": new_data["patient_village"],
      "email": new_data.get('patient_email', None),
      "phone_number": new_data.get('patient_phone_number', None),
      "kin_name": new_data.get('kin_name', None),
      "kin_relation": new_data.get('kin_relation', None),
      "tribe": new_data.get('tribe', None),
      "race": new_data.get('race', None)
    }
  if len(data.data) == 0: #create the patient
    data = supabase.table("Patient").insert(new_patient).execute()
  else: # update the patient
    data = supabase.table("Patient").update(new_patient).eq('fname', patient_fname).eq('lname', patient_lname).eq('sex', patient_sex).eq('birthdate', patient_birthdate).execute()
  
  # get the patient id
  patient_id = data.data[0]['id']
  # get the operator id
  operator_id = new_data['operator_id']
  # get the health center id
  hc_id = new_data['hc_id']
  # get the request physician id
  data = supabase.table("General Practitioner").select("*").eq('fname', new_data['req_phys_fname']).eq('lname', new_data['req_phys_lname']).execute()
  if len(data.data) == 0:
    data = supabase.table("General Practitioner").insert({"fname": new_data['req_phys_fname'], "lname": new_data['req_phys_lname']}).execute()
    req_phys_id = data.data[0]['id']
  else:
    req_phys_id = data.data[0]['id']
  # get the date
  date = new_data['date']
  # get the clinical workup
  clinical_workup = new_data.get('clinical_workup', None)
  # get the stain
  stain = new_data.get('stain', None)
  # get the specimen
  specimen = new_data['specimen']
  # get the operator diagnosis
  op_dx = new_data['operator_dx']

  to_submit = {
    "patient_id": patient_id,
    "operator_id": operator_id,
    "date_biopsy": date,
    "hc_id": hc_id,
    "clinical_workup": clinical_workup,
    "req_phys_id": req_phys_id,
    "stain": stain,
    "specimen": specimen,
    "op_dx": op_dx,
  }
  try:
    data = supabase.table("Submission").insert(to_submit).execute()
    return data.data[0]
  except:
    return []
  

def upload_image(data):
  try:
        base64_image = data.get('base64_image')

        if base64_image:
            image_data = base64.b64decode(base64_image)
            # image = Image.open(BytesIO(image_data))

            p = str(uuid.uuid4()) + ".jpeg"
            response = supabase.storage.from_('testing').upload(file=image_data, path = p, file_options={"content-type": "image/jpeg"})

            return {"message": "Image received and processed successfully"}
        else:
            return {"error": "Invalid base64 image data"}, 400
  except Exception as e:
      return {"error": str(e)}, 500