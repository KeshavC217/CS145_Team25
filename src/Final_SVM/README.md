###TEAM 25 SUBMISSION

This submission contains the required files to regenerate our results for COVID prediction.

Data link:

Data contains:
- Modified training data for Dec 7-13
- Modified testing data to account for lack of Dec 6 data
- Provided training and testing data for Sep 1-26

**How to run**
- The runnable code is contained in model_svr.py
- Inside, there is a function
    - svr(train_path, test_path, isFuture)
    - This takes in the path to the training and testing data, as well as a boolean isFuture
        - True if we want Dec 7-13 predictions
        - False if we want Sept 1-26 predictions
- Simply call this function with the above parameters set as desired, and a csv called team25.csv will be generated
- team25.csv is the required csv
