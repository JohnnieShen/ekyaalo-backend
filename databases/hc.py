import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_hc(new_data):
  data = supabase.table("Health Center").select("*").eq("name", new_data["name"]).eq("county", new_data["county"]).execute()
  if data.data:
    return []
  try:
    data = supabase.table("Health Center").insert(new_data).execute()
    return data.data
  except:
    return []