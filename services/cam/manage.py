import  logging
from flask.cli import FlaskGroup
from sqlalchemy import text

from project import create_app, db

app = create_app()

cli = FlaskGroup(create_app=create_app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#@cli.command("recreate_db")
#def recreate_db():
#    db.drop_all()
#    db.create_all()
#    db.session.commit()


#@app.teardown_appcontext
#def teardown_db(exception):
#    db = g.pop('db', None)
#    if db is not None:
#        db.getConn().close()


@cli.command("health" )
def seed_db():
    """ Check connectivity."""
    logger("Check connection health:")

    with db.engine.connect() as conn:
        conn.execute(text("select 'Hi everything fine, don.t worry'"))
        logger("Total objects : {}".format(conn.execute("SELECT count(*) FROM OBJECTS" ).fetchall()))
        logger("Total statistic : {}".format(conn.execute("SELECT count(*) FROM STATISTIC" ).fetchall()))        
    logger("Database connection health was fine !!!")

if __name__ == "__main__":
    cli()

    

