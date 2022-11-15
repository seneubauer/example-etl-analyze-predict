# import dependencies
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

# locate the config.py file
import sys
sys.path.insert(0, "..")

# instantiate the base
Base = declarative_base()

# define tables
class Gauge_Types(Base):
    __tablename__ = "gauge_types"
    uid = Column(Integer, nullable = False, unique = True, primary_key = True)
    name = Column(String(25), nullable = False)

class Characteristic_Types(Base):
    __tablename__ = "characteristic_types"
    uid = Column(Integer, nullable = False, unique = True, primary_key = True)
    name = Column(String(25), nullable = False)
    is_gdt = Column(Boolean, nullable = False)

class Gauges(Base):
    __tablename__ = "gauges"
    uid = Column(String(25), nullable = False, unique = True, primary_key = True)
    location = Column(String(25), nullable = False)
    type_uid = Column(Integer, ForeignKey("gauge_types.uid"), nullable = False)

class Parts(Base):
    __tablename__ = "parts"
    drawing = Column(String(25), nullable = False, primary_key = True)
    revision = Column(String(5), nullable = False, primary_key = True)
    item = Column(String(25), nullable = False, primary_key = True)
    __tableargs__ = (
        UniqueConstraint(drawing, revision, item)
    )

class Characteristics(Base):
    __tablename__ = "characteristics"
    uid = Column(Integer, nullable = False, unique = True, primary_key = True)
    name = Column(String(50), nullable = False)
    nominal = Column(Float, nullable = False)
    usl = Column(Float, nullable = False)
    lsl = Column(Float, nullable = False)
    part_drawing = Column(String(25), nullable = False)
    part_revision = Column(String(5), nullable = False)
    part_item = Column(String(25), nullable = False)
    type_uid = Column(Integer, ForeignKey("characteristic_types.uid"), nullable = False)
    gauge_uid = Column(String(25), ForeignKey("gauges.uid"), nullable = False)
    __tableargs__ = (
        ForeignKeyConstraint(
            [part_drawing, part_revision, part_item],
            [Parts.drawing, Parts.revision, Parts.item]
        )
    )

# import the confidential information
from config import pg_key, pg_db, pg_host, pg_port, pg_user

# create the database if it doesn't already exist
engine = create_engine(f"postgresql://{pg_user}:{pg_key}@{pg_host}:{pg_port}/{pg_db}", echo = True)
if not database_exists(engine.url):
    create_database(engine.url)

# connect to the database
conn = engine.connect()

# create the tables
Base.metadata.create_all(engine)