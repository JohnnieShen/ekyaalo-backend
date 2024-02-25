import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_patient(new_data):
  data = supabase.table("Patient").select("*").eq("fname", new_data["fname"]).eq("lname", new_data["lname"]).eq("sex", new_data["sex"]).eq("birthdate", new_data["birthdate"]).execute()
  if data.data:
    return []
  try:
    data = supabase.table("Patient").insert(new_data).execute()
    return data.data[0]
  except:
    return None
  
def get_patient(id):
  try:
    data = supabase.table("Patient").select("*").eq("id", id).execute()
    return data.data[0]
  except:
    return None
  
def get_patients():
  try:
    data = supabase.table("Patient").select("*").execute()
    return data.data
  except:
    return None
  
