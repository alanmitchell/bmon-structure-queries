#!/usr/bin/env python3

import sqlite3
import time
import sys
from pathlib import Path
import pytz

try:
    conn_readings = sqlite3.connect('bms_data.sqlite')
    cur_readings = conn_readings.cursor()

    # Delete the old sensor_stats file
    Path('sensor_stats.sqlite').unlink(missing_ok=True)
    input('Hello')

    conn_stats = sqlite3.connect('sensor_stats.sqlite')
    cur_stats = conn_stats.cursor()

    # Create the two tables
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
                print(sensor_id, rdg_ct, mins_ago)
                sql = f"INSERT INTO sensor_info VALUES ('{sensor_id}', {mins_ago}, {rdg_ct})"
                cur_stats.execute(sql)
            except:
                print(f'Problem with {sensor_id}')
                print(sys.exc_info())

except:
    print(sys.exc_info())

finally:
    conn_stats.commit()
    conn_stats.close()
    conn_readings.close()
