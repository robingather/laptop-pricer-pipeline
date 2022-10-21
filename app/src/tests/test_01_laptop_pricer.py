# content of test_sysexit.py
import pandas as pd

# content of test_class.py
import laptop_pricer


class TestDiabetesPredictor:
    def test_predict_single_record(self):
        with open('tests/prediction_request.json') as json_file:
            data = pd.read_json(json_file)
        dp = laptop_pricer.LaptopPricePredictor()
        status = dp.predict_single_record(data)
        assert bool(status[0]) is not None
        assert bool(status[0]) is False
