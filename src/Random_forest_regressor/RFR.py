import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn import preprocessing


def get_training_data(file_path):
    data = pd.read_csv(file_path)
    return data.drop(columns=['Confirmed', 'Deaths']), data[['Confirmed', 'Deaths']]


def get_testing_data(file_path):
    data = pd.read_csv(file_path)
    return data[['Date', 'Province_State']], data[['Confirmed', 'Deaths']]


class RFRModel(object):
    def __init__(self):
        self.train_x = pd.DataFrame()
        self.train_y = pd.DataFrame()
        self.test_x = pd.DataFrame()
        self.test_y = pd.DataFrame()

    def load_data(self, train_file, test_file):
        self.train_x, self.train_y = get_training_data(train_file)
        self.train_x = self.train_x.fillna(self.train_x.mean())
        self.test_x, self.test_y = get_testing_data(test_file)

    def process_data(self, df):
        df['Date'] = pd.to_datetime(df['Date'])
        df["day"] = df['Date'].map(lambda x: x.day)
        df["month"] = df['Date'].map(lambda x: x.month)
        df["year"] = df['Date'].map(lambda x: x.year)
        df["dno"] = df['month'] * 100 + df['day'] * 3
        # This converts the date into a usable integer. Confirmed cases should increase with
        # an increase in date, so using month * 100 + day gives a good system for keeping this consistent


def initial_processing():
    rfr = RFRModel()
    rfr.load_data("../../data/train.csv", "../../data/test.csv")
    rfr.process_data(rfr.train_x)
    rfr.process_data(rfr.test_x)
    return rfr


def simple_predictor():
    rfr = initial_processing()

    # Get the temporary subsets of trainx and trainy
    real_train_x = rfr.train_x[['dno', 'Province_State']]
    real_train_y = rfr.train_y[['Confirmed']]

    le = preprocessing.LabelEncoder()
    real_train_x.Province_State = le.fit_transform(real_train_x.Province_State)

    real_test_x = rfr.test_x[['dno', 'Province_State']]
    real_test_x.Province_State = le.fit_transform(real_test_x.Province_State)

    regr = RandomForestRegressor(n_estimators=200, random_state=0)
    regr.fit(real_train_x, real_train_y.values.ravel())
    print(list(regr.predict(real_test_x)))


if __name__ == '__main__':
    simple_predictor()
