import csv

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
          'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
          'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
          'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
          'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

dates = ["11-23-2020", "11-24-2020", "11-25-2020", "11-26-2020", "11-27-2020", "11-28-2020", "11-29-2020",
         "11-30-2020", "12-01-2020", "12-02-2020", "12-03-2020", "12-04-2020", "12-05-2020", "12-06-2020", "12-07-2020",
         "12-08-2020", "12-09-2020", "12-10-2020", "12-11-2020", "12-12-2020", "12-13-2020"]

with open('modified_test.csv', mode='w') as prediction_file:
    prediction_writer = csv.writer(prediction_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')
    prediction_writer.writerow(['ForecastID', 'Province_State', 'Date', 'Confirmed', 'Deaths'])
    count = 0
    for date in dates:
        for state in states:
            prediction_writer.writerow([str(count), state, date, '-1', '-1'])
            count = count + 1
