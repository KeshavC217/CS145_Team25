import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Perceptron
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


def string_process(x):
    y = x[0].split('-')
    return int(y[0])*100 + int(y[1]) * 3


data = pd.read_csv("../../data/train.csv")
data = data.fillna(data.mean())
data = data[['Date', 'Confirmed']]
data_alabama = data.iloc[::50,:]
X_temp = data_alabama.iloc[:,0:1].values
X = np.array([[string_process(x)] for x in X_temp])
y = data_alabama.iloc[:,1].values
polynomial_features= PolynomialFeatures(degree=2)
Xpol = polynomial_features.fit_transform(X)
reg = LinearRegression().fit(Xpol,y)
plt.plot(X,y)
plt.plot(X,reg.predict(Xpol))

test_data = pd.read_csv("../../data/test.csv")
test_data = test_data[['Date']]
test_data_alabama = test_data.iloc[::50,:]
test_x_temp = test_data_alabama.iloc[:,0:1].values
test_x = np.array([[string_process(x)] for x in test_x_temp])
testx_pol = polynomial_features.fit_transform(test_x)
predicted_y = reg.predict(testx_pol)

plt.plot(test_x, predicted_y)
plt.show()

