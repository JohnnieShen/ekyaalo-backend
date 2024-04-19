import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_path(new_data):
  if check_exists(new_data["fname"], new_data["lname"]):
    return []
  data = supabase.table("Pathologist").insert(new_data).execute()
  return data.data[0] if data else []

def get_pathologists():
  data = supabase.table("Pathologist").select("*").execute()
  return data.data if data else []

def get_pathologist_by_id(path_id):
  data = supabase.table("Pathologist").select("*").eq("id", path_id).execute()
  return data.data[0] if data.data else {}

def patho_update_submission(new_data):
  if not check_path_exists(new_data["path_id"]):
    return []
  if not check_sub_exist(new_data["sub_id"]):
    return []
  signed_date = new_data["signed_date"]
  path_id = new_data["path_id"]
  sub_id = new_data["sub_id"]
  path_dx = new_data["path_dx"]
  data = supabase.table("Submission").update({"path_id": path_id, "signed_date":signed_date, "path_dx":path_dx}).eq("sub_id", sub_id).execute()
  return data.data[0] if data.data else []

def get_path_submissions(path_id):
  if not check_path_exists(path_id):
    return "Pathologist does not exist."
  data = supabase.table("Submission").select("*").eq("path_id", path_id).execute()
  return data.data if data else []
  
# Helper functions
def check_exists(fname, lname):
    try:
      data = supabase.table("Pathologist").select("*").eq("fname", fname).eq("lname", lname).execute()
      return len(data.data) > 0
    except:
      return False  

def check_path_exists(path_id):
  try:
    data = supabase.table("Pathologist").select("*").eq("id", path_id).execute()
    return len(data.data) > 0
  except:
    return False

def check_sub_exist(sub_id):
  try:
    data = supabase.table("Submission").select("*").eq("sub_id", sub_id).execute()
    return len(data.data) > 0
  except:
    return False
      