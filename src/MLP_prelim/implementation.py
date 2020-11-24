import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR


# The point of this approach is to try and predict each data column separately
# Join each predicted column to the test data
# Use a more complicated algorithm to predict testing results

def string_process(x):
    y = x.split('-')
    return int(y[0]) * 100 + int(y[1]) * 3


data_confirmed = pd.read_csv('confirmed_cleaned.csv')
y_confirmed = data_confirmed['Confirmed']
X_confirmed = data_confirmed.drop(columns=['Confirmed'])

test_data = pd.read_csv("../../data/test.csv")
test_date_temp = test_data['Date'].iloc[::50]
test_dates = np.array([string_process(i) for i in test_date_temp]).reshape(-1,1)


def pred_incident_rate(stateno):
    X_date = X_confirmed['Date'].iloc[stateno::50]
    X_incident = X_confirmed['Incident_Rate'][stateno::50]
    X_date = np.array(X_date).reshape(-1,1)
    X_incident = np.array(X_incident)

    reg = SVR(C=500)
    reg.fit(X_date,X_incident)
    pred_y = reg.predict(test_dates)
    return pred_y


def pred_people_tested(stateno):
    X_date = X_confirmed['Date'].iloc[stateno::50]
    X_tested = X_confirmed['People_Tested'][stateno::50]
    X_date = np.array(X_date).reshape(-1,1)
    X_tested = np.array(X_tested)

    reg = LinearRegression()
    reg.fit(X_date,X_tested)
    pred_y = reg.predict(test_dates)
    return pred_y


incident_predictions = np.array([pred_incident_rate(i) for i in range(50)]).T.ravel()
tested_predictions = np.array([pred_people_tested(i) for i in range(50)]).T.ravel()

reg = MLPRegressor(learning_rate_init=0.008)
reg.fit(X_confirmed, y_confirmed)

fin_inc_frame = pd.DataFrame()
fin_inc_frame['Date'] = [string_process(i) for i in test_data['Date']]
fin_inc_frame['Incident_Rate'] = incident_predictions
fin_inc_frame['People_Tested'] = tested_predictions

final_pred = reg.predict(fin_inc_frame)


def prediction_adjuster(state_no):
    start_arr = np.array(y_confirmed.iloc[state_no::50].values)
    start_point = start_arr[len(start_arr)-1]
    curr_pred = final_pred[state_no::50]
    diff = start_point - curr_pred[0]
    curr_pred = curr_pred + diff
    return curr_pred


new_preds = np.array([prediction_adjuster(i) for i in range(50)])
final_pred_2 = new_preds.T.ravel()

def sanity_plot(state_no):
    curr_conf_date = X_confirmed['Date'].iloc[state_no::50]
    curr_conf_pred = y_confirmed.iloc[state_no::50]
    plt.plot(curr_conf_date, curr_conf_pred)

    future_conf_date = fin_inc_frame['Date'].iloc[state_no::50]
    future_conf_pred = final_pred_2[state_no::50]
    plt.plot(future_conf_date, future_conf_pred)

    plt.show()


sanity_plot(47)


