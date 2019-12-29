from django.shortcuts import render
from .forms import UserRegisterForm
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

def landing(request):
    return render( request, 'weather/landing.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        user_info = form.save()
        _id = user_info.id

        flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/JackGood/coding_practice/calendar/google_calendar_weather/weather/credentials.json', 
                SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        print(creds)
        with open('token.pickle.'+str(_id), 'wb') as token:
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
    


    else:
        form = UserRegisterForm()
    return render( request, 'weather/signup.html', {'form': form} )






