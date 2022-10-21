import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import LinearRegression        
import pickle 
import logging 
import argparse

def train_lr (features, model):
    '''train a LinearRegressor with default parameters'''
    
    data = pd.read_csv(features.path+".csv")
    # split into input (X) and output (y) variables
    X = data.loc[:, ["Company","TypeName","Ram","Weight","TouchScreen","IPS","PPI","Cpu_brand","HDD","SSD","Gpu brand","os"]].values
    y = data.loc[:, ['Price_euros']].values
    
    # define model
    step1 = ColumnTransformer(transformers=[
    ('col_tnf',OneHotEncoder(sparse=False,drop='first'),[0,1,7,10,11])
    ],remainder='passthrough')

    step2 = LinearRegression()

    pipe = Pipeline([
        ('step1',step1),
        ('step2',step2)
    ])
    
    pipe.fit(X,y)
    
    logging.info("Fitted model")
    
    model.metadata["framework"] = "LR"
    file_name = model.path + f".pkl"
    with open(file_name, 'wb') as file:  
        pickle.dump(pipe, file)   


#     # Defining and parsing the command-line arguments
# def parse_command_line_arguments():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--features', type=str, help="Input training dataset")
#     parser.add_argument('--model', type=str, help="Output model")
#     args = parser.parse_args()
#     return vars(args)  # The vars() method returns the __dict__ (dictionary mapping) attribute of the given object.


# if __name__ == '__main__':
#     download_data(
#         **parse_command_line_arguments())  # The *args and **kwargs is a common idiom to allow arbitrary number of
#     # arguments to functions