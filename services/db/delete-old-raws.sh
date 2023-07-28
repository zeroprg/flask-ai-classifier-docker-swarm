#!/bin/bash
# use this cronttab -e  command  to add this linu to crontab:
# 0 0 * * * /home/odroid/delete_old_records.sh

# Define PostgreSQL container name and other connection parameters
CONTAINER_NAME=postgres_arm64
DB_USER=odroid
DB_NAME=streamer

# Run the SQL query using psql inside the container
docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME <<EOF
DELETE FROM objects
        WHERE currentime < (EXTRACT(EPOCH FROM NOW()) * 1000) - (14 * 24 * 60 * 60 * 1000);
DELETE FROM statistic
        WHERE currentime < (EXTRACT(EPOCH FROM NOW()) * 1000) - (14 * 24 * 60 * 60 * 1000);
EOF
