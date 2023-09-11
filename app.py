# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
import os
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

################################################
# Database Setup
#################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/tstats/&lt;start&gt;<br>"
        f"/api/v1.0/tstats/&lt;start&gt;/&lt;end&gt;<br>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Find the most recent date in the data set.
    recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date  = dt.date.fromisoformat(recent_date_str)
    # Calculate the date one year from the last date in data set.
    year_before_date = recent_date - dt.timedelta(days=365)
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    # Perform a query to retrieve the date and precipitation scores
    last_12_months = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                filter(Measurement.date >= year_before_date).\
                group_by(Measurement.date).\
                order_by(Measurement.date.asc()).\
                all()
    session.close()
    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    #to a dictionary using date as the key and prcp as the value.
    prcp = {}
    for row in last_12_months:
        prcp[row[0]] = row[1]

    #Return the JSON representation of your dictionary.
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
# Query and return a JSON list of stations from the dataset.
    stations = session.query(Station.station).all()
    session.close()
    data = {}
    for item in stations:
        data[item[0]]=item[1]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
# # Design a query to calculate the total number of stations in the dataset
    station_count = Session.query(Measurement.station, func.count(Measurement.station)).\
                     group_by(Measurement.station).\
                     order_by(func.count(Measurement.station).desc()).all()
    
    session.close()
    print(station_count)
# # Return a JSON list of temperature observations for the previous year.
    return jsonify(tobs)

## Functions for tstats()

@app.route("/api/v1.0/tstats/<string:start>")
def temperature_stats_start(start):
    # For a specified start, Calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
    session = Session(engine)
    
    results = session.query(
        func.min(Measurement.tobs).label("min_temp"),
        func.avg(Measurement.tobs).label("avg_temp"),
        func.max(Measurement.tobs).label("max_temp")
    ).filter(
        Measurement.date >= start
    ).all()
    
    session.close()
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    if results:
        min_temp, avg_temp, max_temp = results[0]
        return jsonify({
            "start_date": start,
            "min_temperature": min_temp,
            "avg_temperature": avg_temp,
            "max_temperature": max_temp
        })
    

@app.route("/api/v1.0/tstats/<string:start>/<string:end>")
def temperature_stats_start_end(start, end):
    # Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    session = Session(engine)
    
    results = session.query(
        func.min(Measurement.tobs).label("min_temp"),
        func.avg(Measurement.tobs).label("avg_temp"),
        func.max(Measurement.tobs).label("max_temp")
    ).filter(
        Measurement.date >= start,
        Measurement.date <= end
    ).all()
    
    session.close()
    
    if results:
        min_temp, avg_temp, max_temp = results[0]
        return jsonify({
            "start_date": start,
            "end_date": end,
            "min_temperature": min_temp,
            "avg_temperature": avg_temp,
            "max_temperature": max_temp
        })
    
if __name__ == "__main__":
    app.run(debug=True)