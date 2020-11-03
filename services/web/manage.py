from flask.cli import FlaskGroup
import logging
from project import create_app, db

import sqlalchemy as sql
from sqlalchemy import text

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("health")
def seed_db():
    """ Check connectivity."""
    print("Check connection health:")
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    
    with db.engine.connect() as conn:
        conn.execute(text("select 'Hi everything fine, don.t worry'"))
        print("Total objects : {}".format(conn.execute("SELECT count(*) FROM OBJECTS" ).fetchall()))
        print("Total statistic : {}".format(conn.execute("SELECT count(*) FROM STATISTIC" ).fetchall()))
        metadata = sql.MetaData()
        objects = sql.Table('objects', metadata, autoload=True, autoload_with=db.engine)

    print("Database connection health was fine !!!")
    



if __name__ == "__main__":
    cli()
