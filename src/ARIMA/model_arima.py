import numpy as np
import sklearn 
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy.integrate import odeint
import math
from statsmodels.tsa.arima.model import ARIMA
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

def arima(train_path, test_path, isFuture=False):
    def predictARIMA(X, p, d, q, day):
        model = ARIMA(X, order=(p,d,q)).fit()
        prediction = model.predict(start = len(X), end = len(X) + days)
        return prediction

    print('loading data...', end='')
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    statesdata = {}
    states = pd.Series.unique(train['Province_State'])
    num_states = len(states)
    for s in states:
        statesdata[s] = train.loc[train['Province_State'] == s ,:]
    print('done')

    if isFuture:
        days = 7
    else:
        days = 26

    print('making state predictions...', end='')
    proj = {}
    for s in states:
        a = statesdata[s].reset_index()
        confirmed = a['Confirmed']
        deaths = a['Deaths']
        
        X, Y = confirmed.values, deaths.values
        forecastC = predictARIMA(X, 3,2,1, days) # BEST PARAMS SO FAR ARE 3,2,1
        forecastD = predictARIMA(Y, 4,2,3, days) # BEST PARAMS SO FAR ARE 4,2,3

        df = {'Confirmed': forecastC, 'Deaths': forecastD}
        
        proj[s] = pd.DataFrame(df)
    print('done')

    print('creating output file...', end='')
    order = test.loc[0:49,'Province_State']
    conf = []
    dead = []
    fid = 0
    for i in range(days):
        for j in order:
            projection = proj[j].iloc[i]
            conf.append(int(projection['Confirmed']))
            dead.append(int(projection['Deaths']))
            fid+=1

    test['Confirmed'] = conf
    test['Deaths'] = dead
    submission = test.drop(columns=['Province_State', 'Date'])
    submission.to_csv('team25.csv', index = False, header = True)
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
arima("../../data/train.csv", "../../data/test.csv")
print('mape: ', give_mape('team25.csv', '../ValidationTester/ground_truth.csv'))



