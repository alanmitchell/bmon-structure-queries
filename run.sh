#!/bin/bash

sqlite3 -header -csv bmon.sqlite < queries/sensors.sql > data/sensors.csv
sqlite3 -header -csv bmon.sqlite < queries/alert-recips.sql > data/alert-recips.csv
sqlite3 -header -csv bmon.sqlite < queries/alerts.sql > data/alerts.csv
sqlite3 -header -csv bmon.sqlite < queries/alert-events.sql > data/alert-events.csv
