# CS145 COVID Prediction Project

This repo contains my solution to CS145's [COVID prediction challenge](https://www.kaggle.com/c/ucla2020-cs145-covid19-prediction/leaderboard)

## Objective

Given COVID statistics from each state, predict the future cases and deaths.

## Team

- Sultan Madkhali (Leader)
- Tejas Bhat
- Keshav Chakrapani
- Harsh Chobisa
- Prithvi Kannan

## Dependencies
- [Python 3](https://www.python.org/downloads/)
- [statsmodels](https://www.statsmodels.org/stable/install.html)

Make sure to run `pip install statsmodels`.

## Data

[Dataset link](https://drive.google.com/drive/folders/13eKpEJaqWpJgI1RQLGqyWJF7UAp-7MZ0?usp=sharing):
- Modified training data for Dec 7-13
- Modified testing data to account for lack of Dec 6 data
- Provided training and testing data for Sep 1-26
- Note: Download this data locally for use with our model

# Usage

Prepare model inputs:

Set `train_path` and `test_path` to appropriate datasets. By default, `isFuture=False`, meaning predict round1, but `isFuture=True` changes the prediction to round2.

NOTE: For round1, calculate MAPE using helper function with crawled ground truth.

Run arima model: `python3 model_arima.py`. 
The output will look as such:
```
$ python3 model_arima.py 
ROUND 1
loading data...done
making state predictions...done
creating output file...done
mape:  0.025305383288031016
ROUND 2
loading data...done
making state predictions...done
creating output file...done
```

