import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Perceptron
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, RobustScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


def string_process(x):
    y = x[0].split('-')
    return int(y[0]) * 100 + int(y[1]) * 3


data = pd.read_csv("../../data/train.csv")
data = data.fillna(data.mean())
data = data[['Date', 'Confirmed']]
test_data = pd.read_csv("../../data/test.csv")
test_data = test_data[['Date']]


def predict_state_confirmed(state_index):
    data_state = data.iloc[state_index::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    polynomial_features = PolynomialFeatures(degree=3)
    reg = SVR(C=1e5, max_iter=1000)
    reg.fit(X, y)
    test_data_state = test_data.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    predicted_y = reg.predict(test_x)
    return predicted_y


def plot_confirmed(state_no, result_matrix):
    data_state = data.iloc[state_no::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    plt.plot(X, y)
    test_data_state = test_data.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    pred_y = result_matrix[state_no]
    plt.plot(test_x, pred_y)
    plt.show()


result_matrix = np.array([predict_state_confirmed(i) for i in range(50)])
plot_confirmed(1, result_matrix)
