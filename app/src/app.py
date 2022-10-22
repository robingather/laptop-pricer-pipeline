from flask import Flask, request, render_template, jsonify
from laptop_pricer import LaptopPricePredictor
import pandas as pd
import json
import sys
import os

app = Flask(__name__)
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
def price_laptop():
    if request.method == "POST":
        print(request)
        print(request.method)
        print(request.form)
        print(type(request.method))
        print(type(request.form.get("Ram")))
        print(request.form.get("Company"), file=sys.stderr)
        print(request.form.get("TypeName"), file=sys.stderr)
        print(request.form.get("Ram"), file=sys.stderr)
        print(request.form.get("Weight"), file=sys.stderr)
        print(request.form.get("TouchScreen"), file=sys.stderr)
        print(request.form.get("IPS"), file=sys.stderr)
        print(request.form.get("PPI"), file=sys.stderr)
        print(request.form.get("Cpu_brand"), file=sys.stderr)
        print(request.form.get("HDD"), file=sys.stderr)
        print(request.form.get("SSD"), file=sys.stderr)
        print(request.form.get("Gpu_brand"), file=sys.stderr)
        print(request.form.get("os"), file=sys.stderr)
        prediction_input = None
        if request.form.get("Company") == None:
            prediction_input = request.get_json()
        else:
            prediction_input = [    
                {
                    "Company": str(request.form.get("Company")),  # getting input with name = ntp in HTML form
                    "TypeName": str(request.form.get("TypeName")),  # getting input with name = pgc in HTML form
                    "Ram": int(request.form.get("Ram")),
                    "Weight": float(request.form.get("Weight")),
                    "TouchScreen": int(1 if request.form.get("TouchScreen") == 'on' else 0),
                    "IPS": int(1 if request.form.get("IPS") == 'on' else 0),
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
        df = pd.read_json(json.dumps(prediction_input), orient='records')
        status = dp.predict_single_record(df)
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        # print(status)
        # print(status[0])
        # print(type(status))
        # print(type(status[0]))
        # print(str(status[0]))
        return status[0], 200

    return render_template("user_form.html")  # this method is called of HTTP method is GET, e.g., when browsing the link


#if __name__ == '__main__':
#    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
print("hAIIII",file=sys.stderr)

if __name__ == "__main__":      
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=False)
