import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_gp(new_data):
  try:
    data = supabase.table("General Practitioner").insert(new_data).execute()
    return data.data
  except:
    return []