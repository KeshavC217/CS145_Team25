# necessary imports
import numpy as np
import pandas as pd
import sklearn 
import matplotlib.pyplot as plt
import scipy
import math
from statsmodels.tsa.statespace.sarimax import SARIMAX

# suppress convergence warnings
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

def arima(train_path, test_path, isFuture=False):
    '''Main driver function for ARIMA. Takes in training and testing path and extra flag to denote future prediction'''

    CASES_PARAMS = (3,2,1)
    DEATH_PARAMS = (4,2,3)
    if isFuture:
        days = 8
    else:
        days = 26

    # --- LOAD AND PREPARE TRAINING AND TESTING DATA ---
    print('loading data...', end='')
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    statesdata = {}
    states = pd.Series.unique(train['Province_State'])
    num_states = len(states)
    for s in states:
        statesdata[s] = train.loc[train['Province_State'] == s ,:]
    print('done')

    # --- MAKE STATE BY STATE PREDICTIONS ---
    print('making state predictions...', end='')
    predictions = {}
    for s in states:
        temp = statesdata[s].reset_index()
        confirmed_cases = temp['Confirmed'].values
        deaths = temp['Deaths'].values
        
        cases_model = SARIMAX(confirmed_cases, order=CASES_PARAMS, enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
        forecasted_cases = cases_model.forecast(days)

        deaths_model = SARIMAX(deaths, order=DEATH_PARAMS, enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
        forecasted_deaths = deaths_model.forecast(days)

        df = {'Confirmed': forecasted_cases, 'Deaths': forecasted_deaths}
        predictions[s] = pd.DataFrame(df)
    print('done')

    # --- COLLATE PREDICTIONS AND WRITE OUTPUT ---
    print('creating output file...', end='')
    state_order = test.loc[0:49,'Province_State']
    pred_cases = []
    pred_dead = []
    fid = 0
    if isFuture:
        base = 1
    else:
        base = 0
    for i in range(base,days):
        for j in state_order:
            projection = predictions[j].iloc[i]
            pred_cases.append(int(projection['Confirmed']))
            pred_dead.append(int(projection['Deaths']))
            fid += 1

    test['Confirmed'] = pred_cases
    test['Deaths'] = pred_dead
    submission = test.drop(columns=['Province_State', 'Date'])
    if isFuture:
        submission.to_csv('team25_round2.csv', index = False, header = True)
    else:
        submission.to_csv('team25_round1.csv', index = False, header = True)

    print('done')


def give_mape(ground_truth_path, prediction_path):
    ground_truth = pd.read_csv(ground_truth_path)
    predictions = pd.read_csv(prediction_path)

    gt_conf = ground_truth['Confirmed']
    gt_dead = ground_truth['Deaths']

    pred_conf = predictions['Confirmed']
    pred_dead = predictions['Deaths']

    total = 0
    for i in range(1300):
        conf_error = float(pred_conf[i] - gt_conf[i]) / float(gt_conf[i])
        dead_error = float(pred_dead[i] - gt_dead[i]) / float(gt_dead[i])
        total = total + abs(conf_error) + abs(dead_error)

    total = total / 2600
    return total


# round1
print('ROUND 1')
arima("../../data/train.csv", "../../data/test.csv")
print('mape: ', give_mape('team25.csv', '../ValidationTester/ground_truth.csv'))

# round2
print('ROUND 2')
# arima("../../data/train_round2.csv", "../../data/test_round2.csv", isFuture=True)
arima("../SVM_round2/modified_train.csv", "../../data/test_round2.csv", isFuture=True)

