import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def get_submissions():
  try:
    data = supabase.table("Submission").select("*").execute()
    return data.data
  except:
    return []



# get the submissions taken by a specific operator
def get_submission(fname,lname):
  # get the operator id
  try:
    data = supabase.table("Operator").select("*").eq("fname", fname).eq("lname", lname).execute()
    operator_id = data.data[0]["id"]
  except:
    return []
  # get the submissions taken by the operator
  try:
    data = supabase.table("Submission").select("*").eq("operator_id", operator_id).execute()
    return data.data
  except:
    return []




# def 
  

