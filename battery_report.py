#!/usr/bin/env python3

""" Creates the battery discharge "report" (a CSV file with sensor and discharge info).
"""

# Controls which sensors appear in the report. 0.06 means that if the battery
# voltage has dropped more than 6%, then the sensor will appear in the report.
DISCHARGE_THRESHOLD = 0.06

import sqlite3
import pandas as pd

conn = sqlite3.connect('bms_data.sqlite')
cursor = conn.cursor()

# make a Dataframe containing the sensor IDs of all sensors in the 
# reading database.
query = "SELECT name FROM sqlite_master WHERE type='table';"
df_all_sensors = pd.read_sql_query(query, conn)
df_all_sensors.columns = ['sensor_id']

# Sensor ID suffixes for battery voltage sensors of interest
battery_suffixes = (
    'Vbat',
    'batteryVoltage',       # Only found at most 2 readings per sensor ID for this suffix.
    'vdd'
)
regex_pattern = '|'.join(battery_suffixes)

# Filter rows where 'column_name' contains any of the battery suffixes
df_bat = df_all_sensors[df_all_sensors['sensor_id'].str.contains(regex_pattern)].copy()

# determine the amount that the voltage has dropped from its highest level,
# in fractional terms
query = 'SELECT val FROM [%s]'
discharge_frac = []
for sensor in df_bat.sensor_id.values:
    df_one = pd.read_sql_query(query % sensor, conn)
    # some of the values may be in millivolts, so convert to volts
    df_one.loc[df_one.val > 100, 'val'] /= 1000.0
    v_charged = df_one.val.quantile(0.99)    # 99th percentile highest voltage
    v_end = df_one.val.values[-1]            # last read voltage
    frac = 1.0 - v_end / v_charged
    discharge_frac.append(frac) 
conn.close()

df_bat['discharge_frac'] = discharge_frac
df_bat.sort_values('discharge_frac', ascending=False, inplace=True)

# filter down to the ones that have discharged too much
dfdead = df_bat.query('discharge_frac > @DISCHARGE_THRESHOLD').copy()

# read in sensor info CSV file created from the 'sensor.sql' script.
dfs = pd.read_csv('data/sensors.csv')

# make a column containing the base sensor ID for each sensor in the file.
# this removes the suffix.
dfs['sensor_base'] = dfs.sensor_id.str.split("_").str[0]

# make a new dataframe with key info for each base sensor ID
def summarize_sensor(group):
    return pd.Series({
        'building': ', '.join(set(group.building_name.values)),
        'sensors': ', '.join(set(group.sensor_name.values)),
        'last_report_minutes': group.last_report_minutes.min()    # best value of the group
    })
dfsb = dfs.groupby('sensor_base').apply(summarize_sensor)

# prepare to merge the prior Dataframe containing dead battery sensors 
dfdead['sensor_base'] = dfdead.sensor_id.str.split("_").str[0]
dfdead.set_index('sensor_base', inplace=True)
dfdead.rename(columns={'sensor_id': 'battery_sensor_id'}, inplace=True)

df_final = dfdead.merge(dfsb, left_index=True, right_index=True).reset_index()
df_final = df_final[['building', 'sensors', 'discharge_frac', 'battery_sensor_id', 'last_report_minutes']]
df_final.sort_values('building', inplace=True)

df_final.to_csv('data/battery-report.csv', index=False)

