import os
from supabase import create_client, Client
from PIL import Image
import base64
from io import BytesIO
import uuid

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
bucket_name = "Beta_4-15-2024"

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
def get_oper_submission(id):
  try:
    data = supabase.table("Submission").select("*").eq('operator_id', id).execute()
    return data.data
  except:
    return []

def get_submission(id):
  try:
    data = supabase.table("Submission").select("*").eq('sub_id', id).execute()
    result = data.data[0]
    result['images'] = retrieve_images(id)
    del result['assoc_images']
    return result
  except Exception as e:
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
  except:
    return []
  
  sub_id = data.data[0]['sub_id']
  slides = new_data['images']
  slide_upload = {}
  failed_imgs = []
  for i,slide in enumerate(slides):
    slidename = slide['slidename']
    imagelist = slide['imagelist']
    type_list = []
    for j,image in enumerate(imagelist):
      encoded_image = image['image']
      type_list.append(image['type'])
      if upload_image(encoded_image, sub_id, slidename, str(j+1), image['type']):
        failed_imgs.append((slidename,j+1))
    slide_upload[slidename] = type_list
  data = supabase.table("Submission").update({"assoc_images": slide_upload}).eq('sub_id', sub_id).execute()
  return data.data[0]

def upload_image(img, sub_id, slidename, img_num, type):
  try:
    image_data = base64.b64decode(img)
    image_name = str(sub_id) + "_" + slidename + "_" + img_num + "_" + type + ".jpeg"
    response = supabase.storage.from_(bucket_name).upload(file=image_data, path = image_name, file_options={"content-type": "image/jpeg"})
    return 0
  except Exception as e:
    return 1

def retrieve_images(sub_id):
  data = supabase.table("Submission").select("*").eq("sub_id", sub_id).execute()
  if len(data.data) == 0:
    return "Submission does not exist"
  img_nums = data.data[0]['assoc_images']
  ret_val = []

  for slide_name, imgs in img_nums.items():
    imagelist = []
    for i,type in enumerate(imgs):
      file_name = str(sub_id) + "_" + slide_name + "_" + str(i+1) + "_" + type + ".jpeg"
      try:
        img_download = supabase.storage.from_(bucket_name).download(file_name)
        base64_encoded = base64.b64encode(img_download).decode('utf-8')
        imagelist.append({
          "type": type,
          "image": base64_encoded
        })
      except:
        continue
      to_add = {
        "slidename": slide_name,
        "imagelist": imagelist
      }
    ret_val.append(to_add)
  return ret_val