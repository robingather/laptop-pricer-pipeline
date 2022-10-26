import os

import pandas as pd
import pickle
from flask import jsonify
from google.cloud import storage
import sys

class LaptopPricePredictor:
    def __init__(self):
        self.model = None

    def download_test_model(self):
        self.model = pickle.load(open('testResources/laptop_pricer_model.pkl', 'rb'))
        print("downloaded test model")
        #return jsonify({'message': " the model was downloaded"}), 200

    # download the model
    def download_model(self):
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

    def predict_single_record(self, prediction_input, test = False):
        print(prediction_input)
        if test:
           self.download_test_model()
        elif not test:
           self.download_model()

        print(prediction_input.values,  file=sys.stderr)
        print(prediction_input.values[0],  file=sys.stderr)
        y_pred = self.model.predict(prediction_input.values)

        result = y_pred[0]
        try:
            result[0]
            result = result[0]
        except IndexError:
            print("is not a list")

        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        if test:
            return result # if I return a jsonified result with 200 http code during testing, it will give the error that the Flask context is not initialized.
        else:
            return jsonify({'result': str(result)}), 200
