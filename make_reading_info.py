#!/usr/bin/env python3

import sqlite3
import time
from datetime import datetime
import sys
from pathlib import Path
import pytz

try:
    conn_readings = sqlite3.connect('bms_data.sqlite')
    cur_readings = conn_readings.cursor()

    # Delete the old sensor_stats database
    Path('sensor_stats.sqlite').unlink(missing_ok=True)

    conn_stats = sqlite3.connect('sensor_stats.sqlite')
    cur_stats = conn_stats.cursor()

    # Create the two tables in the Sensor Stats database
    sql = """CREATE TABLE alert_events (
    ts_unix INTEGER,
    ts TEXT,
    sensor_id TEXT,
    message TEXT
    );"""
    cur_stats.execute(sql)

    sql = """CREATE TABLE sensor_info (
    sensor_id TEXT UNIQUE,
    last_report NUMERIC,
    reading_count INTEGER,
    PRIMARY KEY (sensor_id)
    );"""
    cur_stats.execute(sql)

    # Build the Sensor Information table in the new Stats database.
    # This includes how many minutes ago the sensor last reported, and includes
    # the total reading count for the sensor.
    sql = 'SELECT name FROM sqlite_master WHERE type = "table"'
    for row in cur_readings.execute(sql).fetchall():
        sensor_id = row[0]
        if not sensor_id.startswith('_'):
            try:
                sql = f'SELECT count(*) FROM [{sensor_id}]'
                rdg_ct = cur_readings.execute(sql).fetchone()[0]
                sql = f'SELECT max(ts) FROM [{sensor_id}]'
                mins_ago = (time.time() - cur_readings.execute(sql).fetchone()[0]) / 60.0
                mins_ago = round(mins_ago, 1)
                sql = f"INSERT INTO sensor_info VALUES ('{sensor_id}', {mins_ago}, {rdg_ct})"
                cur_stats.execute(sql)
            except:
                print(f'Problem with {sensor_id}')
                print(sys.exc_info())
    
    # Create an expanded Alert Events table in the Stats database, which adds a field
    # that displays timestamp in human-readable Alaska Time.
    tz_ak = pytz.timezone('US/Alaska')    # want result in Alaska Time
    sql = 'SELECT id, ts, message FROM _alert_log'
    for sensor_id, ts_unix, message in cur_readings.execute(sql).fetchall():
        try:
            ts = datetime.utcfromtimestamp(ts_unix)
            ts = pytz.utc.localize(ts)     # make it timezone aware
            ts = ts.astimezone(tz_ak)         # convert to Alaska time
            ts_text = ts.strftime('%Y-%m-%d %H:%M:%S')
            sql = f"INSERT INTO alert_events VALUES ({ts_unix}, '{ts_text}', '{sensor_id}', '{message}')"
            cur_stats.execute(sql)
        except:
            print(sys.exc_info())

except:
    print(sys.exc_info())

finally:
    conn_stats.commit()
    conn_stats.close()
    conn_readings.close()
