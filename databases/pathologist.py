import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_path(new_data):
  try:
    data = supabase.table("Pathologist").insert(new_data).execute()
    return data.data
  except:
    return []

def get_pathologists():
  try:
    data = supabase.table("Pathologist").select("*").execute()
    return data.data
  except:
    return []

def get_pathologist_by_id(path_id):
  try:
    data = supabase.table("Pathologist").select("*").eq("id", path_id).execute()
    return data.data[0]
  except:
    return {}