import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# DESCRIPTION:
# STATE_NO: 1-> Alabama, 4-> California, etc.
# plot_confirmed-> True if you want to plot cases, false if you want to plot deaths
def sanity_plot(training_path, prediction_path, state_no, plot_confirmed=True):
    train_df = pd.read_csv(training_path)
    pred_df = pd.read_csv(prediction_path)
    result_train = train_df[['Deaths']]
    if plot_confirmed:
        result_train = train_df[['Confirmed']]
    result_pred = pred_df[['Deaths']]
    if plot_confirmed:
        result_pred = pred_df[['Confirmed']]
    state_train = np.array(result_train.iloc[state_no::50]).ravel()
    state_pred = np.array(result_pred.iloc[state_no::50]).ravel()
    plt.plot(np.arange(len(state_train)), state_train)
    plt.plot([238, 239, 240, 241, 242, 243, 244], state_pred)
    plt.show()


sanity_plot("../SVM_round2/modified_train.csv", "../ARIMA/team25_round2.csv", 4, False)

# If you want to plot all 50:
# for i in range(50):
#     sanity_plot("../SVM_round2/modified_train.csv", "../Final_SVM/team25.csv", i)
