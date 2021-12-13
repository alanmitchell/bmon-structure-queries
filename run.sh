#!/bin/bash

sqlite3 -header -csv bmon.sqlite < sensors.sql > data/sensors.csv
sqlite3 -header -csv bmon.sqlite < alerts.sql > data/alerts.csv
