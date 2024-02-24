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
  
# Helper functions
def check_exists(fname, lname):
    try:
      data = supabase.table("Pathologist").select("*").eq("fname", fname).eq("lname", lname).execute()
      return len(data.data) > 0
    except:
      return False  