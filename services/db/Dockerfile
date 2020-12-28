
FROM arm32v7/postgres

# run create.sql on init
COPY create.sql /docker-entrypoint-initdb.d/
CMD psql postgres postgres -f /docker-entrypoint-initdb.d/create.sql
