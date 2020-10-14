import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime

engine = create_engine("sqlite:///Resource/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Mesaurement = Base.classes.Mesaurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# set Flask routes

@app.route("/")
def home():
    prcp_df = pd.read_sql("SELECT date, prcp FROM measurements", con=engine, columns=[["date"],["prcp"]])
    prcp_df["date"] = pd.to_datetime(prcp_df["date"],format="%Y-%M-%D", errors = "coerce")
    prcp_max = str(prcp_df["date"].max().date()-st.timedelta(days=1))
    prcp_year = str(prcp_df["date"].max().date()-dt.timedelta(days=365))
    return (f"Welcome: Climate App<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/percipitation<br/>"
    f"/api/v1.0/tobs><br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end>"
    )

@app.rout("api/v1.0/percipitation")
def percipitation():

    print("Received percipitation API request")

    end_date = session.query(func.max(func.strftime("%Y-%M-%D", Measurement.date))).all()
    max_date1 = end_date[0][0]
    max_date2 = date.datetime.strptime(max_date1, "%Y-%M-%D")
    first_date = max_date2 - datetime.timedalta(365)

    prcp_data = session.query(func.strftime("%Y-%M-%D",Measurement.date), Measurement.prcp).filter(funcstrftime("%Y-%M-%D", Measurement.date) >= first_date).all()

    results_prcp = {}
    for results in percip_data:
        results_prcp[result[0]] = reult[1]

    return jsonify(results_prcp)


@app.rout("api.v1.0/stations") 
def stations():

    print("Received Station API Request")

    stations_data = session.query(Station).all()
    
    stations_list = []
    for station in stations_data:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elecation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("api/v1.0/tobs")
def tobs():

    print("Received tobs API request")

    end_date = session.query(func.max(func.strftime("%Y-%M-%D", Measurement.date))).all()
    max_date1 = end_date[0][0]
    max_date2 = datetime.datetime.strptime(max_date1, "%Y-%M-%D")

    first_date = max_date2 - datetime.timedelta(365)

    results = session.query(Measurement).filter(func.strftime("%Y-%M-%D", Measurement.date) >= first_date).all()

    tobs_list = []
    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["station"] = result.station
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jasonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start):

    print("Received start date API request")

    end_date = session.query(func.max(func.strftime("%Y-%M-%D"))).all()
    max_date2 = end_date[0][0]

    temp = calc_temps(start_date, max_date2)

    return_list = []
    dates_dict = {"start_date": start, "end_date" : max_date2}
    return_list.append(dates_dict)
    return_list.append({"Result": "TMIN", "Temp": temp[0][0]})
    return_list.append({"Result": "TAVG", "Temp": temp[0][1]})
    return_list.append({"Result": "TMAX", "Temp": temp[0][2]})

    return jaonify(return_list)

@app.route("api/v1.0/<start>/<end>")

def start_end(start, end):

    print("Recieved start date and end date API request")

    temp = cal_temps(start, end)

    return_list = []
    dates_dict = {"start_date": start, "end_date" : max_date2}
    return_list.append(dates_dict)
    return_list.append({"Result": "TMIN", "Temp": temp[0][0]})
    return_list.append({"Result": "TAVG", "Temp": temp[0][1]})
    return_list.append({"Result": "TMAX", "Temp": temp[0][2]})

    return Jasonify(return_list)

if __name__ == "__main__":
       app.run(debug = True) 

