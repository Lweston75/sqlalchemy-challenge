  
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#weather app
app = Flask(__name__)


latest_date = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())
latest_date = list(np.ravel(latestDate))[0]

latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
latest_year = int(dt.datetime.strftime(latest_date, '%Y'))
latest_month = int(dt.datetime.strftime(latest_date, '%m'))
latest_day = int(dt.datetime.strftime(latest_date, '%d'))

year_before = dt.date(latest_year, latest_month, latest_day) - dt.timedelta(days=365)
year_before = dt.datetime.strftime(year_before, '%Y-%m-%d')





@app.route("/")
def home():
    return (f"Climate API<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/precipitaton<br/>"
            f"/api/v1.0/temperature<br/>"
            f"/api/v1.0/datesearch/2015-05-30<br/>"
            f"/api/v1.0/datesearch/2015-05-30/2016-01-30<br/>"
            f"~ data available from 2010-01-01 to 2017-08-23<br/>"

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                      .filter(Measurement.date > year_before)
                      .order_by(Measurement.date)
                      .all())
    
    precipData = []
    for result in results:
        precip_dict = {result.date: result.prcp, "Station": result.station}
        precip_data.append(precip_dict)

    return jsonify(precip_data)

@app.route("/api/v1.0/temperature")
def temperature():

    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
                      .filter(Measurement.date > year_before)
                      .order_by(Measurement.date)
                      .all())

    temp_data = []
    for result in results:
        temp_dict = {result.date: result.tobs, "Station": result.station}
        temp_data.append(temp_dict)

    return jsonify(tempData)

@app.route('/api/v1.0/datesearch/<start_date>')
def start(start_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
                       .group_by(Measurement.date)
                       .all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["TMIN"] = result[1]
        date_dict["TAvg"] = result[2]
        date_dict["TMAX"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

@app.route('/api/v1.0/datesearch/<start_date>/<end_date>')
def startEnd(start_date, end_date):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date)
                       .group_by(Measurement.date)
                       .all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["TMIN"] = result[1]
        date_dict["TAVG"] = result[2]
        date_dict["TMAX"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

if __name__ == "__main__":
    app.run(debug=True)