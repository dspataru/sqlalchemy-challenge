# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    
    # List all of the available routes
    return (
        f'Welcome to the Hawaii Climate API!<br/><br/><br/>'
        f'Available Routes:<br/><br/>'
        f'1. Daily Precipitation in Hawaii for last 12 Months: /api/v1.0/precipitation<br/>'
        f'2. List of Active Weather Stations: /api/v1.0/stations<br/>'
        f'3. Dates and Temperature from Most Active Station in the Previous Year: /api/v1.0/tobs<br/>'
        f'4. Temperature Stats from Start Date (yyyy-mm-dd): /api/v1.0/start_date<br/>'
        f'5. Temperature Stats from Date Range (yyyy-mm-dd): /api/v1.0/start_date/end_date<br/>'
    )

# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary 
# using date as the key and prcp as the value.
@app.route('/api/v1.0/precipitation')
def precipitation():
    
    # Creating a session from Python to the database
    session = Session(engine)
    
    start_date = '2016-08-23'
    sel = [measurements.date, func.sum(measurements.prcp)]
    precipitation_query = session.query(*sel).\
        filter(measurements.date >= start_date).\
            group_by(measurements.date).\
                order_by(measurements.date).all()
    
    session.close()
        
    precip = []
    precip_dict = {}
    for date, daily_total_precip in precipitation_query:
        precip_dict['Date'] = date
        precip_dict['Precipitation'] = daily_total_precip
        precip.append(precip_dict)
        
    # Return the JSON representation of your dictionary.
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():
    
    # Creating a session from Python to the database
    session = Session(engine)
    
    sel = [Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation]
    station_query = session.query(*sel).all()
    session.close() 
    
    station_list = []
    station_dict = {}
    for station, name, lat, long, ele in station_query:
        station_dict['Station'] = station
        station_dict['Name'] = name
        station_dict['Latitude'] = lat
        station_dict['Longitude'] = long
        station_dict['Elevation'] = ele
        station_list.append(station_dict)
        
            
    # Return a JSON list of stations from the dataset.
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    
    # Creating a session from Python to the database
    session = Session(engine)
    
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    most_recent_date_query = session.query(measurements.date).\
        order_by(measurements.date.desc()).first()[0]
    
    most_recent_date = dt.datetime.strptime(most_recent_date_query, '%Y-%m-%d')
    query_date = dt.date(most_recent_date.year - 1, most_recent_date.month, most_recent_date.day)
    
    sel = [measurements.date, measurements.tobs]
    station_temps_query = session.query(*sel).\
        filter(measurements.date >= query_date, measurements.station == 'USC00519281').\
            group_by(measurements.date).\
                order_by(measurements.date).all()
    session.close()
    
    dates_temps_list = []
    dates_temps_dict = {}
    for date, temp in station_temps_query:
        dates_temps_dict['Date'] = date
        dates_temps_dict['Temperature'] = temp
        dates_temps_list.append(dates_temps_dict)
    
    # Return a JSON list of temperature observations for the previous year.
    return jsonify(dates_temps_list)

@app.route('/api/v1.0/<start>')
def no_end_date_provided(start):
    
    # Creating a session from Python to the database
    session = Session(engine)
    
    # For a specified start, calculate TMIN, TAVG, and TMAX for all 
    # the dates greater than or equal to the start date.
    query = session.query(measurements.date, func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
        filter(measurements.date >= start).\
            group_by(measurements.date).all()
    
    temp_stats = []
    temp_dict = {}
    for date, min, max, avg in query:
        temp_dict['Date'] = date
        temp_dict['Min'] = min
        temp_dict['Max'] = max
        temp_dict['Average'] = avg
        temp_stats.append(temp_dict)
    
    # Return a JSON list of the minimum temperature, the average temperature, 
    # and the maximum temperature for a specified start or start-end range.
    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def end_date_provided(start, end):
    
    # Creating a session from Python to the database
    session = Session(engine)
    
    # For a specified start date and end date, calculate TMIN, TAVG, and TMAX 
    # for the dates from the start date to the end date, inclusive.
    temp_stats_query = session.query(measurements.date, func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
        filter(measurements.date >= start).\
            filter(measurements.date <= end).\
                group_by(measurements.date).all()
    
    temp_stats = []
    temp_dict = {}
    for date, min, max, avg in temp_stats_query:
        temp_dict['Date'] = date
        temp_dict['Min'] = min
        temp_dict['Max'] = max
        temp_dict['Average'] = avg
        temp_stats.append(temp_dict)
        
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug = True)