import os

from flask import Flask, request, render_template, jsonify
from laptop_pricer import LaptopPricePredictor
import pandas as pd
import json

app = Flask(__name__)
app.config["DEBUG"] = True
dp = LaptopPricePredictor()

@app.route('/laptop_pricer/model', methods=['PUT'])  # trigger updating the model
def refresh_model():
    return dp.download_model()


@app.route('/laptop_pricer', methods=['POST'])  # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_input = request.get_json()
    return dp.predict_single_record(prediction_input)


# A decorator used to tell the application
# which URL is associated function
@app.route('/price_laptop', methods=["GET", "POST"])
def check_diabetes():
    if request.method == "POST":
        prediction_input = [
            {
                "Company": str(request.form.get("Company")),  # getting input with name = ntp in HTML form
                "TypeName": str(request.form.get("TypeName")),  # getting input with name = pgc in HTML form
                "Ram": int(request.form.get("Ram")),
                "Weight": float(request.form.get("Weight")),
                "TouchScreen": str(request.form.get("TouchScreen")),
                "IPS": str(request.form.get("IPS")),
                "PPI": float(request.form.get("PPI")),
                "Cpu_brand": str(request.form.get("Cpu_brand")),
                "HDD": int(request.form.get("HDD")),
                "SSD": int(request.form.get("SSD")),
                "Gpu brand": str(request.form.get("Gpu_brand")),
                "os": str(request.form.get("os"))
            }
        ]
        print(prediction_input)
        dp = LaptopPricePredictor()
        df_json = json.dumps(prediction_input)
        status = dp.predict_single_record(df_json)
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(status[0])}), 200

    return render_template("user_form.html")  # this method is called of HTTP method is GET, e.g., when browsing the link


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)

app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
