# bmon-structure-queries
SQL queries related to BMON structure that are saved to CSV files.

The program `sqlite3` must be available in the PATH.  The script also uses Python3
to create a needed SQLite database file.

Execute the `run.sh` file to run the queries and create the CSV files. CSV files are 
written into the data/ folder.

There must be `bmon.sqlite` (BMON Django file) and `bms_data.sqlite` (BMON Sensor Reading)
files, usually through a symbolic link, in
the root directory of this repository for the queries to be applied to.
