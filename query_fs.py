import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from score import Score
from google.cloud.firestore_v1.base_query import FieldFilter, Or

"""
FIRESTORE Data Access
"""

def open_firestore_db():
    # Use the sdk credentials
    cred = credentials.Certificate('ps_firestore_cred.json') # grabs key from parent local folder

    # Initialize access to firestore database
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def open_db_collection(db):
    user_ref = db.collection("Users")
    return user_ref     


#####THINGS TO CONSIDER########
# def run_query(raw, db):
#     rows = build_query(raw, db)
#     vehicle_rows = []
#     # if build_query returns string do not call to.dict return string
#     if isinstance(rows, str):
#         vehicle_rows.append(rows)
#         return vehicle_rows
#     # formats returned list of document snaps into a list of Vehicle dictionaries
#     for r in rows:
#         vehicle_rows.append(format_vehicle(r.to_dict(), r.id))
#     return vehicle_rows