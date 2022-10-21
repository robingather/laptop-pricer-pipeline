import pandas as pd
import logging 
import sys
from sklearn.model_selection import train_test_split as tts

def train_test_split(dataset, dataset_train, dataset_test):
    '''train_test_split'''
    logging.basicConfig(stream=sys.stdout, level=logging.INFO) 
    
    alldata = pd.read_csv(dataset.path, index_col=0)
    train, test = tts(alldata, test_size=0.15)
    train.to_csv(dataset_train.path + ".csv" , index=False, encoding='utf-8-sig')
    test.to_csv(dataset_test.path + ".csv" , index=False, encoding='utf-8-sig')

    # Defining and parsing the command-line arguments
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, help="Input dataset")
    parser.add_argument('--dataset_train', type=str, help="ame of the file to be used to store training data")
    parser.add_argument('--dataset_test', type=str, help="Name of the file to be used to store testing data")
    args = parser.parse_args()
    return vars(args)  # The vars() method returns the __dict__ (dictionary mapping) attribute of the given object.


if __name__ == '__main__':
    download_data(
        **parse_command_line_arguments())  # The *args and **kwargs is a common idiom to allow arbitrary number of
    # arguments to functions