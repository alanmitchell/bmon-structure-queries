#!/bin/bash

sqlite3 -header -csv bmon.sqlite < queries/sensors.sql > data/sensors.csv
sqlite3 -header -csv bmon.sqlite < queries/alerts.sql > data/alerts.csv
