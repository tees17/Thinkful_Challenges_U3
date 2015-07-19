import requests
import pandas as pd
import datetime
import sqlite3 as lite


cities = {"Boston": '42.331960,-71.020173',
          "Chicago": '41.837551,-87.681844',
          "Minneapolis": '44.963324,-93.268320',
          "Seattle": '47.620499,-122.350876',
          "Washington": '8.904103,-77.017229'
          }

end=datetime.datetime.now()

con = lite.connect('weather.db')
cur = con.cursor()

cities.keys()
with con:
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Boston REAL, Chicago REAL, Minneapolis REAL, Seattle REAL, Washington REAL);')

start = end - datetime.timedelta(days=30)
with con:
    while start < end:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(start.strftime('%S')),))
        start += datetime.timedelta(days=1)

api_key="ca20973d07061e42cfb1f4932d7c8bbc"

for k,v in cities.iteritems():
    start = end - datetime.timedelta(days=30) #set value each time through the loop of cities
    while start < end:
    	weather=requests.get("https://api.forecast.io/forecast/" + api_key + "/"  + v + "," + start.strftime('%Y-%m-%dT%H:%M:%S'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(weather.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + start.strftime('%S'))
            start += datetime.timedelta(days=1) #increment query_date to the next day

con.close()