
FROM arm32v7/postgres

# run create.sql on init

USER postgres
RUN whoami
ADD  create.sql /docker-entrypoint-initdb.d/
ENTRYPOINT ["docker-entrypoint.sh"]
EXPOSE 5432
CMD ["postgres"]