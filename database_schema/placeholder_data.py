# import dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd

# resolve sqlalchemy/numpy issue
import numpy
from psycopg2.extensions import register_adapter, AsIs
def adapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, adapt_numpy_float64)
register_adapter(numpy.int64, adapt_numpy_int64)

# locate config.py
import sys
sys.path.insert(0, "..")

# import confidential information
from config import pg_key, pg_db, pg_host, pg_port, pg_user

# create the sqlalchemy engine
engine = create_engine(f"postgresql://{pg_user}:{pg_key}@{pg_host}:{pg_port}/{pg_db}", pool_pre_ping = True, echo = False)

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

# instantiate the sqlalchemy session
session = Session(engine)

# add the data in order
for index, row in unit_types_df.iterrows():
    session.add(unit_types(uid = row["uid"], name = row["name"]))

for index, row in gauge_types_df.iterrows():
    session.add(gauge_types(uid = row["uid"], name = row["name"]))

for index, row in characteristic_types_df.iterrows():
    session.add(characteristic_types(uid = row["uid"], name = row["name"], is_gdt = row["is_gdt"]))

for index, row in stations_df.iterrows():
    session.add(stations(uid = row["uid"], name = row["name"]))

for index, row in machines_df.iterrows():
    session.add(machines(uid = row["uid"], pad = row["pad"], name = row["name"]))

for index, row in locations_df.iterrows():
    session.add(locations(uid = row["uid"], station_uid = row["station_uid"], machine_uid = row["machine_uid"]))

for index, row in gauges_df.iterrows():
    session.add(gauges(uid = row["uid"], location_uid = row["location_uid"], type_uid = row["type_uid"]))

for index, row in parts_df.iterrows():
    session.add(parts(drawing = row["drawing"], revision = row["revision"], item = row["item"]))

for index, row in characteristics_df.iterrows():
    session.add(characteristics(uid = row["uid"], name = row["name"], nominal = row["nominal"], usl = row["usl"], lsl = row["lsl"], part_drawing = row["part_drawing"], part_revision = row["part_revision"], part_item = row["part_item"], unit_type_uid = row["unit_type_uid"], type_uid = row["type_uid"], gauge_uid = row["gauge_uid"]))

# commit the changes
session.commit()

# close the session
session.close()