import os
from supabase import create_client, Client

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