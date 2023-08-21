# sqlalchemy-challenge - Honolulu, Hawaii Trip Planning

![hawaii_image]()

## Table of Contents
* [Background]()
* [Analyze and Explore the Climate Data]()
** [Precipitation Analysis]()
** [Station Analysis]()
* [Designing the Climate App]()

## Background

This repository contains a short climate analysis for Honolulu, Hawaii to aid in trip planning for a holiday vacation using climate data taken from different stations in Hawaii between 2010-2017. The climate data used in the analysis is split into two tables:
1. [hawaii_measurements.csv](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii_measurements.csv): table containing the station, date, precipitation amount, and temperature observations.
2. [hawaii_stations.csv](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii_stations.csv): table containing the station, name, latitude, longitude, and elevation of the stations.

The analysis was performed using Python and SQLAlchemy. Specifically, SQLAlchemy ORM queries, Pandas, and Matplotlib are used to perform a two-part analysis on the climate data, and design a basic climate web app.

The SurfsUp directory contains two folders, (1) [Resources](https://github.com/dspataru/sqlalchemy-challenge/tree/main/SurfsUp/Resources) and (2) [images](https://github.com/dspataru/sqlalchemy-challenge/tree/main/SurfsUp/images), [climate_starter.ipynb](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/climate_starter.ipynb) Jupyter Notebook, and the [app.py](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/app.py) Python script for the web application. The Resources folder contains the database [hawaii.sqlite](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii.sqlite), and the two csv files mentioned above. The images folder contains the output files for the Jupyter notebook file.

#### Key Words
SQLAlchemy, Python, ORM queries, Pandas, Matplotlib, SQLite database, Flask API, JSON, API data, Flask Application, Jupyter Notebook

## Analyze and Explore the Climate Data

Python and SQLAlchemy are used to perform a basic climate analysis and data exploration of the climate database: [hawaii.sqlite](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii.sqlite). Using the SQLAlchemy create_engine() function, we connect to the SQLite database. The automap_base() function was used to reflect the tables into classes which were then saved in Python as "station" and "measurement". Python was then linked to the database by creating a SQLAlchemy session. The session was closed at the end of the analysis.

### Precipitation Analysis

The measurement table was used to perform the precipitation analysis as it contains the precipitation data for each station in Honolulu, Hawaii, and for each day between 2010-2017. The goal of this analysis was to summarize the previous 12 months of precipitation data by querying the previous 12 months of data. The first step was to find the most recent date in the dataset. This was done by querying the measurements table and ordering the data by date in descending order. The first entry was outputted and the result was '2017-08-23'. This string was stored as a variable to be called later in the analysis.

Next, a query was designed to retrieve the last 12 months of precipitation data starting from the most recent data point in the database and calculating the date one year from the most recent date in the data set. This was calcualted to be '2016-08-23' using the datatime library. The measurements data set was then filtered by all entries where the date was newer than the query date which is '2016-08-23', and the date and precipitation information was extracted for all entries. The results were saved into a Pandas DataFrame and the column names were set to 'Date (YYYY-MM-DD)' and 'Precipitation (inches)'. Some of the values in the Pandas DataFrame had missing values (NA) which were dropped so the data could be plot and summary statistics could be calculated from the precipitation data. After the data was cleaned, the DataFrame was sorted by date and plotted using Matplot lib. The result is shown below. As can be seen from the graph, in the past 12 months, Honolulu, Hawaii has had the most amount of rainfall in September 2016, end of January 2017, April 2017, and July 2017.

![annual_precip_hawaii](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/images/annual_precipitation_hawaii.png)

Pandas describe() function was used to calculate the summary statistics for the precipitation data:
![summary_stats](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/images/summary_stats.png)

### Station Analysis

Both the station and measurement tables were used to perform the station analysis. After performing a query on the stations table, we learned that Honolulu, Hawaii has nine active stations collecting precipitation and temperature data. To determine which station is the most active station, the stations and observation counts were listed in descending order and USC00519281 (WAIHEE 837.5, HI US) was calcuated to be the most active station. Below was the result of the query:
[('USC00519281', 2772),
 ('USC00519397', 2724),
 ('USC00513117', 2709),
 ('USC00519523', 2669),
 ('USC00516128', 2612),
 ('USC00514830', 2202),
 ('USC00511918', 1979),
 ('USC00517948', 1372),
 ('USC00518838', 511)]

Using the most active station ID, the lowest, highest, and average temperature were calculated to be 54.0 F, 85.0 F, and 71.66 F, respectively. The last 12 months of temperature observation data for the USC00519281 station were queried and the results were plotted as a histogram as seen below.

![temps_active_station](https://github.com/dspataru/sqlalchemy-challenge/blob/main/SurfsUp/images/annual_temps_at_most_active_station.png)

## Designing the Climate App

After completing the queries on the station and measurement data sets, a Flask API was designed. Using Flask, the following routes were created:
1. '/' : This is the homepage that lists all of the available routes.
2. '/api/v1.0/precipitation' : This route converts the query results from the precipitation analysis (i.e. only the last 12 months of data) to a dictionary using date as the key and prcp as the value. This route returns the JSON representation of the dictionary.
3. '/api/v1.0/stations' : This route returns a JSON list of stations from the dataset.
4. '/api/v1.0/tobs' : This route queries the dates and temperature observations of the most-active station for the previous year of data and return a JSON list of temperature observations for the previous year.
5. '/api/v1.0/<start> and /api/v1.0/<start>/<end>' : This query returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range. For a specified start, TMIN, TAVG, and TMAX were calculated for all the dates greater than or equal to the start date. For a specified start date and end date, TMIN, TAVG, and TMAX were calculated for the dates from the start date to the end date, inclusive.
