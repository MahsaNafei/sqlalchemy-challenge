# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# Define the root route
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>Precipitation data for the last year<br/><br/>"
        f"/api/v1.0/stations<br/>List of weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Temperature observations for the most active station in the last year<br/><br/>"
        f"/api/v1.0/start_date<br/>Minimum, average, and maximum temperature statistics starting from the specified date(YYYY-MM-DD)<br/><br/>"
        f"/api/v1.0/start_date/end_date<br/>Minimum, average, and maximum temperature statistics within the specified date range"
    )



# Define the route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a database session
    session = Session(engine)
    
    # Calculate the date one year ago
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d").date()
    last_year_date = most_recent_date - dt.timedelta(days=365)

    # Query precipitation data for the last year
    data_last_year = session.query(measurement.date, measurement.prcp, measurement.station).\
        filter(measurement.date >= last_year_date).all()
    
    # Close the database session
    session.close()

    # Create a dictionary to store the precipitation data
    precipitation_dict = {}
    for date, prcp, station_name in data_last_year:
        if date not in precipitation_dict:
            precipitation_dict[date] = []
        if prcp != None:
            precipitation_dict[date].append({
                'prcp': prcp,
                'station': station_name
            })

    # Return the precipitation data as JSON
    return jsonify(precipitation_dict)



# Define the route for station data
@app.route("/api/v1.0/stations")
def stations():
    # Create a database session
    session = Session(engine)
    
    # Query and list the available weather stations
    station_data = session.query(Station.station, Station.name).all()

    # Close the database session
    session.close()

    station_list = []
    for station,name in station_data:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_list.append(station_dict)

    # Return the station data as JSON
    return jsonify(station_list)



# Define the route for temperature data for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Create a database session
    session = Session(engine)

    # Find the most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).\
    order_by(func.count(measurement.station).desc()).first()[0]
    
    # Calculate the date one year ago for the most active station
    most_recent_date_active_station = session.query(func.max(measurement.date)).\
            filter(measurement.station == most_active_station).scalar()
    most_recent_date_active_station = dt.datetime.strptime(most_recent_date_active_station, "%Y-%m-%d").date()
    last_year_date_active_station = most_recent_date_active_station - dt.timedelta(days=365)

    # Query temperature observations for the most active station in the last year
    most_active_station_last_year = session.query(measurement.date, measurement.tobs).\
                filter(measurement.station == most_active_station).\
                filter(measurement.date >= last_year_date_active_station).all()
    
    # Close the database session
    session.close()

    # Create a list to store the temperature data
    temperatures_list = []
    for date, temp in most_active_station_last_year:
        if temp != None:
            temp_dict = {}
            temp_dict[date] = temp
            temperatures_list.append(temp_dict)

    # Return the temperature data as JSON
    return jsonify(temperatures_list)





# Define the route for temperature data within a date range
@app.route("/api/v1.0/<start>", defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")


def start_end(start, end):
    # Create a database session
    session = Session(engine)

    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]


    if end != None:

        # Query temperature statistics (min, avg, max) for the specified date range
        temperature_data = session.query(*sel).\
            filter(measurement.date >= start).filter(measurement.date <= end).all()
    else:
        # Query temperature statistics (min, avg, max) for the specified start date (without end date)
        temperature_data = session.query(*sel).\
            filter(measurement.date >= start).all()

    # Close the database session
    session.close()

    # Initialize variables for error handling
    no_data = False
    temperature_list = []

    # Iterate through the temperature data
    for tmin, tavg, tmax in temperature_data:
        if tmin is None or tavg is None or tmax is None:
            no_data = True

        # Append the temperature data to the list
        temperature_list.append({
            'TMIN': tmin,
            'TAVG': tavg,
            'TMAX': tmax
        })

    if no_data:
        # Handle the case where no temperature data is found
        return jsonify({"error": "No valid temperature data found for the given date range. Try another date range."}), 404
    else:
        # Return the temperature data as JSON
        return jsonify(temperature_list)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
