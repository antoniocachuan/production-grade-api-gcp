import os
from flask import Flask
from flask import request, jsonify

from google.cloud import firestore
from firebase_admin import credentials, firestore, initialize_app

from google.cloud import logging

app = Flask(__name__)

logging_client = logging.Client()

cred = credentials.Certificate('credentials/credentials.json')
default_app = initialize_app(cred)

# The name of the log to write to
log_name = 'my-log'

@app.route("/customer/<id>", methods=["GET"])
def get_transactions(doc):
    masked_doc = masking(doc)
    
    # Selects the log to write to
    logger = logging_client.logger(log_name)

    # Writes the log entry
    logger.log_text(hashed_doc)
    print('Customer ID: {}'.format(id))

    import sys
    sys.stdout.flush()
    
    db = firestore.client()
    users_ref = db.collection(u'customer')

    query = users_ref.where(
        u'id', u'==', 
        u'{}'.format(id)
        )
    
    data = []

    for doc in query.stream():
        data.append(doc.to_dict())

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
