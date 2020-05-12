'''Data retrieved from https://covidtracking.com/api/v1/states/daily.csv '''

import io
import pandas as pd
import requests
import numpy as np
from matplotlib import pyplot
import datetime as dt

url = ('https://covidtracking.com/api/v1/states/daily.csv')

states_dict = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


def usa_data_extractor():
    '''Input: None
       Output: Pandas DataFrame'''
    # Retrieve data from the URL
    urlData = requests.get(url).content
    dataset = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
    return dataset


def usa_data_cleaner(df):
    '''Input: Pandas DataFrame
       Output: Pandas DataFrame'''
    # Drop irrelevant data and remove duplicates
    df = df.drop(['totalTestResults',
                  'dateChecked',
                  'positiveIncrease',
                  'negativeIncrease',
                  'totalTestResultsIncrease',
                  'deathIncrease',
                  'hospitalizedIncrease',
                  'hospitalizedCurrently',
                  'posNeg',
                  'hospitalizedCumulative'],
                 axis=1)
    df['country'] = 'United States of America'
    df = df.drop_duplicates(
        subset=[
            'date',
            'state',
            'positive',
            'recovered',
            'death'],
        keep=False)

    # Reformatting dates and adding state full name column
    for i in range(len(df)):
        date = str(df.loc[i, 'date'])
        date = date[:4] + '-' + date[4:6] + '-' + date[6:8]
        year, month, day = map(int, date.split('-'))
        date = dt.date(year, month, day)
        df.loc[i, 'date'] = date
        df.loc[i, 'state_name'] = states_dict[df.loc[i, 'state']]
        df

    # Renaming columms
    df = df.rename(
        columns={
            "state": "state_code",
            "state_name": "state",
            "positive": "confirmed",
            "total": "tested",
            "death": "fatal"})
    df = df[['date',
             'state_code',
             'state',
             'country',
             'confirmed',
             'negative',
             'inIcuCurrently',
             'onVentilatorCurrently',
             'recovered',
             'fatal',
             'hospitalized',
             'tested',
             'fips']]

    return df


def generate_usa_data():
    return usa_data_cleaner(usa_data_extractor())


def visualize_usa_data(data):
    data = data.iloc[::-1]
    data = data.reset_index()
    data = data.drop(['index', 'tested', 'negative', 'fips'],
                     axis=1)  # Remove data irrelevant to the plot

    print("Data for the United States of America")
    data.hist()  # Plot histogram for the whole country
    data.plot()  # Plot curve for the whole country
    pyplot.show()

    # Plot data for every state
    for state_id in states_dict.keys():
        print(states_dict[state_id])
        state_data = data[data['state_code'] == state_id]
        state_data = state_data[::-1]
        state_data.hist()
        state_data.plot()
        pyplot.show()
