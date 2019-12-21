import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import json
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events', ]
POSTAL_CODE_ENDPOINT = 'http://dataservice.accuweather.com/locations/v1/postalcodes/search?'
FORECAST_ENDPOINT = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day'
API_KEY = 'tFebxs08CTJJGx1E3HwSpIEqGGElXsaN'
ZIP_CODE = '20147'



def remove_event(service,_id):
    event_id = service.events().delete(calendarId='primary', eventId=_id).execute()


def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API

    location_api_call = '{}apikey={}&q={}'.format(POSTAL_CODE_ENDPOINT,
                                                   API_KEY,
                                                   ZIP_CODE)

    location_response = requests.get(location_api_call)
    location_key = location_response.json()[0]['Key']

    forecast_api_call = '{}/{}?apikey={}'.format(FORECAST_ENDPOINT,location_key,API_KEY)

    forecast_response = requests.get(forecast_api_call)

    #print(forecast_response.json())

    events = []
    timezone = { 'timeZone': 'America/Los_Angeles'}
    daily_forecasts = forecast_response.json()['DailyForecasts']
    for forecast in daily_forecasts:
        event ={}
        start = {}
        end = {}
        high = int(forecast['Temperature']['Maximum']['Value'])
        low = int(forecast['Temperature']['Minimum']['Value'])
        weather = forecast['Day']['IconPhrase']
        event_summary = '{} {} / {}'.format(weather,high,low)

        event['summary'] = event_summary
        date = forecast['Date'].split('T')[0]
        
        start['date'] = date
        start['timeZone'] = timezone

        end['date'] = date
        end['timeZone'] = timezone

        event['start'] = start
        event['end'] = end
        events.append(event)
    '''      
    event = {
      'summary': 'Sunny and 75',
      'start': {
        'date': '2019-12-15',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'date': '2019-12-15',
        'timeZone': 'America/Los_Angeles',
      },
    }
    '''


    
    with open('events/current.txt', 'r') as calendar_ids:
        for _id in calendar_ids:
            print(_id)
            remove_event(service,_id.strip())
    

    with open('events/current.txt', 'w') as calendar_ids:
        for event in events:
            event = service.events().insert(calendarId='primary', body=event).execute()
            calendar_ids.write(event.get('id')+'\n')




if __name__ == '__main__':
    main()
