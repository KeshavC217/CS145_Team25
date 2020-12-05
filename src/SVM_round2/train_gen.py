import csv
import pandas as pd


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
          'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
          'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
          'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
          'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

dates = ["11-23-2020", "11-24-2020", "11-25-2020", "11-26-2020", "11-27-2020", "11-28-2020", "11-29-2020",
         "11-30-2020", "12-01-2020", "12-02-2020", "12-03-2020"]

count = 11250

with open('train_add.csv', mode='w') as prediction_file:
    prediction_writer = csv.writer(prediction_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                   lineterminator='\n')
    prediction_writer.writerow(['ID','Province_State','Date','Confirmed','Deaths','Recovered','Active','Incident_Rate','People_Tested','People_Hospitalized','Mortality_Rate','Testing_Rate','Hospitalization_Rate'])
    for date in dates:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'+date+'.csv'
        df = pd.read_csv(url)
        more_states = df['Province_State']
        conf = df['Confirmed']
        deaths = df['Deaths']
        for i in range(len(more_states)):
            if more_states[i] in states:
                prediction_writer.writerow([str(count), more_states[i], date, conf[i], deaths[i], str(-1),str(-1),str(-1),str(-1),str(-1),str(-1),str(-1),str(-1)])
                count+=1
