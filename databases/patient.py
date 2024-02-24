import os
from supabase import create_client, Client
from datetime import date
from heapq import *
import threading

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_patient(data):
  try:
    data = supabase.table("Patient").insert(data).execute()
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
  
