# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# Use Flask to create your routes.

# Routes
# /
# Home page.
# List all routes that are available.

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        
        f"Welcome!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )  



@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query the dates and precipitation from the last year.
    query_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rainfall = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > query_date).\
        order_by(Measurement.date).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precip_dict = []
    for result in rainfall:
        row = {}
        row["date"] = rainfall[0]
        row["prcp"] = rainfall[1]
        precip_dict.append(row)

    # Return the JSON representation of your dictionary.
    return jsonify(precip_dict)



@app.route("/api/v1.0/stations")
def station():
    
    # Query stations
    stations = session.query(Station.name, Station.station)
    station = pd.read_sql(stations.statement, stations.session.bind)
    
    # Return a JSON list of stations from the dataset.
    return jsonify(station.to_dict())


@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query dates and temperature of the most active station for the last year.
    query_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp_query = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.date > last_year).\
        order_by(Measurements.date).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    temp_dict = []
    for result in temperature:
        row = {}
        row["date"] = temp_query[0]
        row["tobs"] = temp_query[1]
        temp_dict.append(row)

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(temp_dict)



# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")
def temp_stats(start):
    
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
        filter(Measurement.date >= start).all()

    summary = list(np.ravel(summary_stats))
    
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(summary)


@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):
    
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    summary_stats = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
        filter(Measurement.date.between(start,end)).all()
    
    summary = list(np.ravel(summary_stats))

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(summary)



if __name__ == "__main__":
    app.run(debug=True)
