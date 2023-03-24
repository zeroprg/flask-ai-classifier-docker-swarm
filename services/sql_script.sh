#!/bin/bash

# Set the Postgres SQL commands to be executed
sql_commands="DELETE FROM statistic WHERE currentime < extract(epoch from now() - interval '120 hours') * 1000; DELETE FROM objects WHERE currentime < extract(epoch from now() - interval '120 hours') * 1000;"

# Execute the commands using the psql command line tool
psql -U odroid -d streamer -c "$sql_commands"
