# import dependencies for flask
from flask import Flask, render_template, jsonify

# import dependencies for sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

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

# instantiate the flask app
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# landing page
@app.route("/")
def IndexRoute():
    return render_template("index.html")

# request list of all unique drawings
@app.route("/get_all_unique_drawings/")
def Get_All_Unique_Drawings():

    # start the database session
    session = Session(engine)

    # query the database
    results = session.query(parts.drawing).all()

    # close the session
    session.close()

    # interpret the results
    if results is None:
        return { "status": "not_ok", "response": "Error within the Flask server or database query." }
    else:
        output = []
        for drawing in results:
            if drawing[0] not in output:
                output.append(drawing[0])
        
        # return the output
        return { "status": "ok", "response": output }

# request list of associated unique revisions
@app.route("/get_associated_unique_revisions/<drawing>/")
def Get_Associated_Unique_Revisions(drawing:str):

    # start the database session
    session = Session(engine)

    # query the database
    results = session.query(parts.revision)\
        .filter(parts.drawing == drawing).all()
    
    # close the session
    session.close()

    # interpret the results
    if results is None:
        return { "status": "not_ok", "response": "Error within the Flask server or database query." }
    else:
        output = []
        for revision in results:
            if revision[0] not in output:
                output.append(revision[0])
        
        # return the output
        return { "status": "ok", "response": output }

# request list of associated unique items
@app.route("/get_associated_unique_items/<drawing>/")
def Get_Associated_Unique_Items(drawing:str):

    # start the database session
    session = Session(engine)

    # query the database
    results = session.query(parts.item)\
        .filter(parts.drawing == drawing).all()
    
    # close the session
    session.close()

    # interpret the results
    if results is None:
        return { "status": "not_ok", "response": "Error within the Flask server or database query." }
    else:
        output = []
        for item in results:
            if item[0] not in output:
                output.append(item[0])
        
        # return the output
        return { "status": "ok", "response": output }

# request characteristics for drawing/revision/item
@app.route("/get_characteristics/<drawing>/<revision>/<item>/")
def Get_Characteristics(drawing:str, revision:str, item:str):

    # define the return features
    features = [
        characteristics.name,
        characteristics.nominal,
        characteristics.usl,
        characteristics.lsl,
        characteristics.part_drawing,
        characteristics.part_revision,
        characteristics.part_item,
        unit_types.name,
        characteristic_types.name,
        characteristic_types.is_gdt,
        gauges.uid,
        gauge_types.name]

    # start the database session
    session = Session(engine)

    # query the database
    results = session.query(*features)\
        .join(unit_types, (characteristics.unit_type_uid == unit_types.uid))\
        .join(characteristic_types, (characteristics.type_uid == characteristic_types.uid))\
        .join(gauges, (characteristics.gauge_uid == gauges.uid))\
        .join(gauge_types, (gauges.type_uid == gauge_types.uid))\
        .filter(characteristics.part_drawing == drawing)\
        .filter(characteristics.part_revision == revision)\
        .filter(characteristics.part_item == item).all()
    
    # close the session
    session.close()

    # interpret the results
    if results is None:
        return { "status": "not_ok", "response": "Error within the Flask server or database query." }
    else:
        output = []
        i = 0
        for name, nominal, usl, lsl, part_drawing, part_revision, part_item, unit_name, characteristic_name, is_gdt, gauge, gauge_type in results:
            output.append({
                "index": i,
                "name": name,
                "nominal": nominal,
                "usl": usl,
                "lsl": lsl,
                "part_drawing": part_drawing,
                "part_revision": part_revision,
                "part_item": part_item,
                "unit_name": unit_name,
                "characteristic_name": characteristic_name,
                "is_gdt": is_gdt,
                "gauge": gauge,
                "gauge_type": gauge_type
            })
            i += 1
        
        # return the output
        return { "status": "ok", "response": output }

# run the flask server
if __name__ == "__main__":
    app.run(debug = True, port = 8000)