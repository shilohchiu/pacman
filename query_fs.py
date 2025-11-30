"""
query_fs initalizes and allows for access to firestore database

query_fs is imported by classes
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from score import Score

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
    #if a document exists just add score to scores and check if updated high score
    if doc_exist:
        #check if score is new overall high score
        document = doc_exist.from_dict()

        if document["high_score"] < score:
            user_ref.document(initial).update({"high_score":score},{"scores":score})

        user_ref.document(initial).update({"scores":score})

    #otherwise create a score and add to_dict to database
    else:
        new_data = Score(initial, high_score = score, scores = [score], curr_score = score)
        user_ref.document(initial).set(new_data.to_dict())

def view_scores(user_ref, initial):
    user_doc = user_ref.document(initial).get()
    user_dict = user_doc.to_dict()
    if user_dict:
        user_scores = user_dict["scores"]
        return user_scores
    user_scores = ["User does not exist"]
    return user_scores

def rt_high_score(user_ref):
    top_doc = user_ref.order_by("high_score", direction=firestore.Query.DESCENDING).limit(1).get()
    top_score = top_doc[0].to_dict()["high_score"]
    return top_score

def is_high_score(user_ref):
    top_ten_doc = user_ref.order_by("high_score",
                                    direction=firestore.Query.DESCENDING).limit(10).get()
    lowest_high_score = top_ten_doc[9].to_dict()["high_score"]
    return lowest_high_score

def top_ten_scores(user_ref):
    top_ten = {}
    top_ten_doc = user_ref.order_by("high_score",
                                    direction=firestore.Query.DESCENDING).limit(10).get()
    for doc in top_ten_doc:
        doc_id = doc.id
        score = doc.to_dict()

        top_ten[doc_id]= score["high_score"]

    return top_ten
