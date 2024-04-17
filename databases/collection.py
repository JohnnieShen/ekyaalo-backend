import os
from supabase import create_client, Client
from PIL import Image
import base64
from io import BytesIO
from uuid import uuid4

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
bucket_name = "Data_Collection"

def upload_image(img, case_no, slidename, img_num, mag, type):
  try:
    image_data = base64.b64decode(img)
    image_name = case_no + "-" + slidename + "-" + img_num + "-" + mag + "-" + type + ".jpeg"
    response = supabase.storage.from_(bucket_name).upload(file=image_data, path = image_name, file_options={"content-type": "image/jpeg"})
    return 0
  except Exception as e:
    return 1

def upload_case(new_data):
  case_id = new_data['case_id']
  slides = new_data['slides']
  slide_upload = {}
  failed_imgs = []
  for i,slide in enumerate(slides):
    slidename = slide['slidename']
    imagelist = slide['imagelist']
    slide_upload[slidename] = len(imagelist)
    for j,image in enumerate(imagelist):
      mag1 = image['mag1']
      mag2 = image['mag2']
      if upload_image(mag1, case_id, slidename, str(j+1), "10X", image['type']):
        failed_imgs.append((slidename,j+1,"10X"))
      if upload_image(mag2, case_id, slidename, str(j+1), "40X", image['type']):
        failed_imgs.append((slidename,j+1,"40X")) 
  data = {
    "case_id": case_id,
    "slides": slide_upload
  }     
  try:
    data = supabase.table("Data Collection").insert(data).execute()
    ret_val = data.data[0]
    ret_val["failed_imgs"] = failed_imgs
    return ret_val
  except:
    return []