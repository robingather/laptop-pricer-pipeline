# content of test_sysexit.py
import pandas as pd

# content of test_class.py
import laptop_pricer


class TestLaptopPricer:
    def test_predict_single_record(self):

        with open('testResources/prediction_request.json') as json_file:
            data = pd.read_json(json_file, orient='records')
        dp = laptop_pricer.LaptopPricePredictor()
        print(data)
        print(data.values)
        print("testing")
        y_pred = dp.predict_single_record(data,test=True)
        print("prediction=",y_pred)

        result = y_pred
        try:
            result[0]
            result = result[0]
        except IndexError:
            print("whoops")         

        print("assertion 1")
        assert result is not None
        print("assertion 2")
        assert str(int(result)).isnumeric() # should be a number
        print("assertion 3")
        assert result > 0 # you shouldn't be paid to buy a laptop
