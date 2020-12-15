import csv
import pandas as pd


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
          'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
          'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
          'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
          'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

dates = ['09-01-2020', '09-02-2020', '09-03-2020', '09-04-2020', '09-05-2020', '09-06-2020', '09-07-2020', '09-08-2020', '09-09-2020', '09-10-2020', '09-11-2020', '09-12-2020', '09-13-2020', '09-14-2020', '09-15-2020', '09-16-2020', '09-17-2020', '09-18-2020', '09-19-2020', '09-20-2020', '09-21-2020', '09-22-2020', '09-23-2020', '09-24-2020', '09-25-2020', '09-26-2020']
dates = ['12-07-2020','12-08-2020','12-09-2020','12-10-2020','12-11-2020','12-12-2020','12-13-2020',]
count = 0

with open('ground_truth.csv', mode='w') as prediction_file:
    prediction_writer = csv.writer(prediction_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')
    prediction_writer.writerow(['ForecastID','Confirmed','Deaths'])
    for date in dates:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'+date+'.csv'
        df = pd.read_csv(url)
        more_states = df['Province_State']
        conf = df['Confirmed']
        deaths = df['Deaths']
        for i in range(len(more_states)):
            if more_states[i] in states:
                prediction_writer.writerow([str(count),conf[i], deaths[i]])
                count+=1
