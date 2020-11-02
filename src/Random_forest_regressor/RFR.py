import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer


def get_training_data(file_path):
    data = pd.read_csv(file_path)
    return data.drop(columns=['Confirmed', 'Deaths']), data[['Confirmed', 'Deaths']]


class RFRModel(object):
    def __init__(self):
        self.train_x = pd.DataFrame()
        self.train_y = pd.DataFrame()
        self.test_x = pd.DataFrame()
        self.test_y = pd.DataFrame()

    def load_data(self, train_file, test_file):
        self.train_x, self.train_y = get_training_data(train_file)
        self.train_x = self.train_x.fillna(self.train_x.mean())


rfr = RFRModel()
rfr.load_data("../../data/train.csv", None)
print(rfr.train_x.head(5))
print(rfr.train_y.head(5))
