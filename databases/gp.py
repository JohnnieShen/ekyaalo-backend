import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_gp(new_data):
  if check_exists(new_data["fname"], new_data["lname"]):
    return []
  data = supabase.table("General Practitioner").insert(new_data).execute()
  return data.data[0] if data else []

def get_gp():
  data = supabase.table("General Practitioner").select("*").execute()
  return data.data if data else []

def get_gp_by_id(path_id):
  data = supabase.table("General Practitioner").select("*").eq("id", path_id).execute()
  return data.data[0] if data.data else {}

# Helper functions
def check_exists(fname, lname):
    try:
      data = supabase.table("General Practitioner").select("*").eq("fname", fname).eq("lname", lname).execute()
      return len(data.data) > 0
    except:
      return False  