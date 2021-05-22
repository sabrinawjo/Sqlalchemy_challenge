# 1. import Flask
from flask import Flask
from flask import json
from flask.json import jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return "Routes: <br> /api/v1.0/precipitation <br> /api/v1.0/stations <br> /api/v1.0/tobs <br> /api/v1.0/&lt;start&gt; <br> /api/v1.0/&lt;start&gt;/&lt;end&gt;"


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    data = session.query(Measurement.date, Measurement.prcp)
    session.close()
    date_dict = dict()
    for day, precp in data.all():
        date_dict[day]=precp
    return jsonify(date_dict)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    stationlist = list(np.ravel(stations))
    return jsonify(stationlist)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    activestations = session.query(Measurement.station, Measurement.date, Measurement.tobs) \
        .filter(Measurement.station == 'USC00519281').all()
    session.close()
    list=[]
    tobs_dict = {}
    for num, day, temp in activestations:
        tobs_dict["Station Num"]=num
        tobs_dict["Date"]=day
        tobs_dict["Temperature"]=temp
        list.append(tobs_dict)
    return jsonify(list)


if __name__ == "__main__":
    app.run(debug=True)

