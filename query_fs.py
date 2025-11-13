import firebase_admin
from firebase_admin import credentials, firestore
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

def add_score(user_ref, initial, score):
    #query database
    query = user_ref.where(filter=FieldFilter("initial", "==", initial))
    doc_exist = query.get()
    print(doc_exist)
    #if a document exists just add score to scores and check if updated high score
    if (doc_exist):
        #check if score is new overall high score
        document = doc_exist.from_dict()

        if (document["high_score"] < score):
            user_ref.document(initial).update({"high_score":score},{"scores":score})

        user_ref.document(initial).update({"scores":score})
        
    #otherwise create a score and add to_dict to database
    else:
        new_data = Score(initial, high_score = score, scores = [score], curr_score = score)
        user_ref.document(initial).set(new_data.to_dict())

def top_ten_scores(user_ref):
    top_ten = {}
    top_ten_doc = user_ref.order_by("high_score", direction=firestore.Query.DESCENDING).limit(10).get()
    for doc in top_ten_doc:
        
        score = doc.to_dict()
        print(score)
        top_ten[score["initial"]] = score["high_score"]

    return top_ten
