from flask.cli import FlaskGroup
from flask import jsonify
import logging
from project import create_app, db # use it for CLI
from project import  db
from project.api.main import main_blueprint
import sqlalchemy as sql
from sqlalchemy import text


app = create_app()
cli = FlaskGroup(create_app=create_app) # use it just for testing 


@cli.command("health") # CLI
@main_blueprint.route("/health", methods=["GET"])
def seed_db():
    """ Check connectivity."""
    print("Check connection health:")
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    objects_rows = statistic_rows = 0

    with db.engine.connect() as conn:
        conn.execute(text("select 'Hi everything fine, don.t worry'"))
        objects_rows = conn.execute("SELECT count(*) FROM OBJECTS" ).fetchall()
        print("Total objects : {}".format(objects_rows[0][0]))
        statistic_rows = conn.execute("SELECT count(*) FROM STATISTIC" ).fetchall()
        print("Total statistic : {}".format(statistic_rows[0][0]))
        print("Database connection health was fine !!!")  
        return jsonify(
            {"Total objects": objects_rows[0][0],  "statistic table rows": statistic_rows[0][0]})

if __name__ == "__main__":
    cli()
    
