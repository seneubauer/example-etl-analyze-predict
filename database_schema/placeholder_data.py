# import dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd

# locate config.py
import sys
sys.path.insert(0, "..")

# import confidential information
from config import pg_key, pg_db, pg_host, pg_port, pg_user

# create the sqlalchemy engine
engine = create_engine(f"postgresql://{pg_user}:{pg_key}@{pg_host}:{pg_port}/{pg_db}", pool_pre_ping = True, echo = True)

# reflect the database
base = automap_base()
base.prepare(engine, reflect = True)

# instantiate the database tables
unit_types = base.classes.unit_types
gauge_types = base.classes.gauge_types
characteristic_types = base.classes.characteristic_types
stations = base.classes.stations
machines = base.classes.machines
locations = base.classes.locations
gauges = base.classes.gauges
parts = base.classes.parts
characteristics = base.classes.characteristics

# read in the mock data
unit_types_df = pd.read_csv("../resources/unit_types.csv")
gauge_types_df = pd.read_csv("../resources/gauge_types.csv")
characteristic_types_df = pd.read_csv("../resources/characteristic_types.csv")
stations_df = pd.read_csv("../resources/stations.csv")
machines_df = pd.read_csv("../resources/machines.csv")
locations_df = pd.read_csv("../resources/locations.csv")
gauges_df = pd.read_csv("../resources/gauges.csv")
parts_df = pd.read_csv("../resources/parts.csv")
characteristics_df = pd.read_csv("../resources/characteristics.csv")