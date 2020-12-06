import pandas as pd


# USAGE: team25.csv is the csv we want to test (our predictions), ground truth doesn't change
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


print(give_mape("ground_truth.csv", "team25.csv"))
