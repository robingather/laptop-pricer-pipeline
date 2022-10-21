import json
import os

import pandas as pd
import pickle
from flask import jsonify
from google.cloud import storage
import sys

class LaptopPricePredictor:
    def __init__(self):
        self.model = None

    # download the model
    def download_model(self):
        print("thank the lord u made it here")
        project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
        model_repo = os.environ.get('MODEL_REPO', 'Specified environment variable is not set.')
        model_name = os.environ.get('MODEL_NAME', 'Specified environment variable is not set.')
        client = storage.Client(project=project_id)
        bucket = client.get_bucket(model_repo)
        blob = bucket.blob(model_name)
        blob.download_to_filename('local_model.pkl')
        self.model = pickle.load(open('local_model.pkl', 'rb'))
        print("downloaded model")
        return jsonify({'message': " the model was downloaded"}), 200

    def predict_single_record(self, prediction_input):
        print(prediction_input)
        #if self.model is None:
        #    self.download_model()
        #print(json.dumps(prediction_input))
        #df = pd.read_json(json.dumps(prediction_input), orient='records')
        print("hEY", file=sys.stderr)
        print(prediction_input.values,  file=sys.stderr)
        print(prediction_input.values[0],  file=sys.stderr)
        y_pred = self.model.predict(prediction_input.values)
        print(y_pred[0])
        print(type(y_pred[0]))
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': float(y_pred[0])}), 200
