import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_operator(new_data):
  if check_exists(new_data["fname"], new_data["lname"]):
    return []
  data = supabase.table("Operator").insert(new_data).execute()
  return data.data[0] if data else []

def get_operators():
  data = supabase.table("Operator").select("*").execute()
  return data.data if data else []

def get_operator_by_id(path_id):
  data = supabase.table("Operator").select("*").eq("id", path_id).execute()
  return data.data[0] if data.data else {}

def login_operator(fname, lname, hc_name):
  op_exists = supabase.table("Operator").select("*").eq("fname", fname).eq("lname", lname).execute()

  if not op_exists.data: # create the user
    op_exists = add_operator({"fname": fname, "lname": lname})
  else:
    op_exists = op_exists.data[0]
  
  op_fname = op_exists["fname"]
  op_lname = op_exists["lname"]
  op_id = op_exists["id"]

  hc_exists = supabase.table("Health Center").select("*").eq("name", hc_name).execute()
  try:
    hc_id = hc_exists.data[0]["id"]
    return {"fname": op_fname, "lname": op_lname, "hc_id": hc_id, "op_id": op_id, "hc_name": hc_name}
  except:
    return []
  
# Helper functions
def check_exists(fname, lname):
    try:
      data = supabase.table("Operator").select("*").eq("fname", fname).eq("lname", lname).execute()
      return len(data.data) > 0
    except:
      return False  