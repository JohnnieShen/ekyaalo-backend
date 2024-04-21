import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_usability(new_data):
    to_upload = {
        "capture_image": new_data["captureImage"],
        "determine_adequacy": new_data["determineAdequacy"],
        "enter_patient_info": new_data["enterPatientInfo"],
        "login": new_data["login"],
        "navigate_clusters": new_data["navigateClusters"],
        "provide_action": new_data["provideAction"],
        "review_records": new_data["reviewRecords"],
        "select_cluster": new_data["selectCluster"],
        "setup_and_calibration": new_data["setupAndCalibration"],
        "stop_capture": new_data["stopCapture"],
        "sync_to_internet": new_data["syncToInternet"],
        "tutorial": new_data["tutorial"]
    }
    try:
        result = supabase.table("Usability").insert(to_upload).execute()
        return result.data[0]
    except Exception as e:
        return []