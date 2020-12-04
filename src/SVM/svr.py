import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import SVR
import csv


def string_process(x):
    y = x[0].split('-')
    return int(y[0]) * 100 + int(y[1]) * 3


def predict_state_confirmed(state_index, data_given, test_data_given):
    data_state = data_given.iloc[state_index::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    ### Comment for old model
    copy_y = np.copy(y)
    orig_state = copy_y[len(y) - 1]
    for i in range(1, len(y)):
        copy_y[len(copy_y) - i] = copy_y[len(copy_y) - i] - copy_y[len(copy_y) - i - 1]
    copy_y[0] = copy_y[1]
    ###
    polynomial_features = PolynomialFeatures(degree=3)
    reg = SVR(C=2000)
    reg.fit(X, copy_y)
    test_data_state = test_data_given.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    predicted_y = reg.predict(test_x)
    ### Comment for old model
    predicted_y[0] = orig_state
    for i in range(1, len(predicted_y)):
        predicted_y[i] += predicted_y[i - 1]
    predicted_y = predicted_y
    ###
    return predicted_y


def predict_state_dead(state_index, data_given, test_data_given):
    data_state = data_given.iloc[state_index::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    polynomial_features = PolynomialFeatures(degree=3)
    param = y[len(y) - 1] * 5
    reg = SVR(C=param)
    reg.fit(X, y)
    test_data_state = test_data_given.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    predicted_y = reg.predict(test_x)
    temp = np.floor(len(predicted_y) / 2)
    if predicted_y[-1] < predicted_y[int(temp)]:
        newreg = LinearRegression()
        newX = X[len(X) - 10:]
        newY = y[len(y) - 10:]
        newreg.fit(newX, newY)
        predicted_y = newreg.predict(test_x)
        diff = newY[-1] - 2*predicted_y[0] + predicted_y[1]
        predicted_y += diff
    # TODO: OPTIONALLY GO WITH EITHER LINREG OR SVR BASED ON IF LAST ELEMENT IS GREATER THAN MID
    # TODO: IF USING LINREG, USE BIAS ADJUSTER
    return predicted_y


def plot_confirmed(state_no, result_matrix_given, data_given, test_data_given):
    data_state = data_given.iloc[state_no::50, :]
    X_temp = data_state.iloc[:, 0:1].values
    X = np.array([[string_process(x)] for x in X_temp])
    y = data_state.iloc[:, 1].values
    plt.plot(X, y)
    test_data_state = test_data_given.iloc[::50, :]
    test_x_temp = test_data_state.iloc[:, 0:1].values
    test_x = np.array([[string_process(x)] for x in test_x_temp])
    pred_y = result_matrix_given[state_no]
    plt.plot(test_x, pred_y)
    plt.show()


data = pd.read_csv("../../data/train.csv")
data = data.fillna(data.mean())
data_dead = data[['Date', 'Deaths']]
data = data[['Date', 'Confirmed']]
test_data = pd.read_csv("../../data/test.csv")
test_data = test_data[['Date']]

result_matrix_confirmed = np.array([predict_state_confirmed(i, data, test_data) for i in range(50)])
result_matrix_dead = np.array([predict_state_dead(i, data_dead, test_data) for i in range(50)])

# This code plots the predictions for confirmed, for a state number of choice:
#plot_confirmed(43, result_matrix_confirmed, data, test_data)
plot_confirmed(8, result_matrix_dead, data_dead, test_data)
# #This code writes to csv
with open('basic_pred_x.csv', mode='w') as prediction_file:
    prediction_writer = csv.writer(prediction_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')

    prediction_writer.writerow(['ForecastID','Confirmed','Deaths'])
    index = range(1300)
    confirmed_vals = result_matrix_confirmed.T.ravel()
    death_vals = result_matrix_dead.T.ravel()
    for i in index:
        prediction_writer.writerow([str(i), str(confirmed_vals[i]), str(death_vals[i])])
