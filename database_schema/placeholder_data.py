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
gauge_types = base.classes.gauge_types
characteristic_types = base.classes.characteristic_types
gauges = base.classes.gauges
parts = base.classes.parts
characteristics = base.classes.characteristics

# define mock data for 'gauge_types'
gauge_types_list = [
    "Caliper",
    "Bore Micrometer",
    "Depth Gauge",
    "Roughness Gauge"
    "CMM",
    "Vision System"
]
gauge_types_df = pd.DataFrame({
    "uid": [i for i in range(len(gauge_types_list))],
    "name": gauge_types_list
})

# define mock data for 'characteristic_types'
characteristic_types_names = [
    "form",
    "distance",
    "angle",
    "diameter",
    "radius",
    "position",
    "concentricity",
    "coaxiality",
    "circularity",
    "cylindricity",
    "straightness",
    "flatness",
    "perpendicularity",
    "parallelism",
    "total_runout",
    "circular_runout",
    "profile_surface",
    "profile_line",
    "angularity",
    "symmetry",
    "size"
]
characteristic_types_isgdt = [
    False,
    False,
    False,
    False,
    False,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True,
    True
]
characteristic_types_df = pd.DataFrame({
    "uid": [i for i in range(len(characteristic_types_names))],
    "name": characteristic_types_names,
    "is_gdt": characteristic_types_isgdt
})