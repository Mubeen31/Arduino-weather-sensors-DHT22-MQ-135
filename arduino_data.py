import serial
import csv
from datetime import datetime
import os
from google.cloud import bigquery

# copy the port from your Arduino editor
PORT = 'COM4'
ser = serial.Serial(PORT, 9600)

while True:
    message = ser.readline()
    data = message.strip().decode()
    split_string = data.split(',')  # split string
    inside_humidity = float(split_string[0])  # convert first part of string into float
    inside_temperature = float(split_string[1])  # convert second part of string into float
    inside_co2 = int(split_string[2])  # convert third part of string into float
    outside_humidity = float(split_string[3])  # convert fourth part of string into float
    outside_temperature = float(split_string[4])  # convert fifth part of string into float
    outside_co2 = int(split_string[5])  # convert sixth part of string into float
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    # ==================== Google BigQuery =======================
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'weatherdata1.json'
    client = bigquery.Client()
    table_id = 'weatherdata1.WeatherSensorsData1.SensorsData1'
    rows_to_insert = [
        {u'DateTime': dt_string,
         u'InsideHumidity': inside_humidity,
         u'InsideTemperature': inside_temperature,
         u'InsideCO2': inside_co2,
         u'OutsideHumidity': outside_humidity,
         u'OutsideTemperature': outside_temperature,
         u'OutsideCO2': outside_co2
         }
    ]
    insert_row = client.insert_rows_json(table_id, rows_to_insert)
    if insert_row == []:
        print('New row have been added:' + dt_string, inside_humidity, inside_temperature, inside_co2,
              outside_humidity, outside_temperature, outside_co2)
    else:
        print(f'Encountered errors while inserting rows: {insert_row}')

    # ==================== Google BigQuery =======================

    with open("humidity_temperature_airquality_data.csv", "a", newline='\n') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([dt_string, inside_humidity, inside_temperature, inside_co2,
                         outside_humidity, outside_temperature, outside_co2])
