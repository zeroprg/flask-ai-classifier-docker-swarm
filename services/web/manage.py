from flask.cli import FlaskGroup
import logging
from project import create_app
from project.db import api 
from flask import g

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    #db.drop_all()
    #db.create_all()
    db.session.commit()


#@app.teardown_appcontext
#def teardown_db(exception):
#    db = g.pop('db', None)
#    if db is not None:
#        db.getConn().close()

@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    #db.session.add(User(username="michael", email="michael@notreal.com"))
    db.session.commit()

@cli.command("ipaddress" )
def seed_db():
    """ Set ipaddress."""
    print("Hited ipaddress")
    #db.session.add(User(username="michael", email="michael@notreal.com"))
    #db.session.commit()


if __name__ == "__main__":
    cli()
