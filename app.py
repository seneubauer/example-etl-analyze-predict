# import dependencies for flask
from flask import Flask, render_template

# import dependencies for sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# import confidential information
from config import pg_key, pg_db, pg_host, pg_port, pg_user

# create the sqlalchemy engine
engine = create_engine(f"postgresql://{pg_user}:{pg_key}@{pg_host}:{pg_port}/{pg_db}", pool_pre_ping = True, echo = True)

# reflect the database
base = automap_base()
base.prepare(engine, reflect = True)

# instantiate the database tables
gauge_types = base.classes.gauge_types
characteristic_types = base.classes.characteristic_types
gauges = base.classes.gauges
parts = base.classes.parts
characteristics = base.classes.characteristics

# instantiate the flask app
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# landing page
@app.route("/")
def IndexRoute():
    return render_template("index.html")



# run the flask server
if __name__ == "__main__":
    app.run(debug = True)