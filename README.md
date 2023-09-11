# sqlalchemy-challengeM10 Challenge
This challenge uses Python and SQLAlchemy to do a basic climate analysis and data exploration of a climate database. Using SQLAlchemy ORM queries, Pandas, and Matplotlib the following steps were executed:
-Use the SQLAlchemy create_engine() function to connect to SQLite database.
-Use the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.
-Link Python to the database by creating a SQLAlchemy session.
Part 1: Analyze and explore climate data
Data analyisis:
-Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.
Precipitation Analysis
1.	Find the most recent date in the dataset.
2.	Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
3.  Plot results
Station Analysis
1.	Design a query to calculate the total number of stations in the dataset.
2.	Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
o	List the stations and observation counts in descending order.
3.	Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
4.	Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
o	Filter by the station that has the greatest number of observations.
o	Query the previous 12 months of TOBS data for that station.
o	Plot the results as a histogram with bins=12, as the following image shows

Part 2: Design Your Climate App
Use Flask to create routes as follows:
1.	/
o	Start at the homepage.
o	List all the available routes.
2.	/api/v1.0/precipitation
o	Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
o	Return the JSON representation of your dictionary.
3.	/api/v1.0/stations
o	Return a JSON list of stations from the dataset.
4.	/api/v1.0/tobs
o	Query the dates and temperature observations of the most-active station for the previous year of data.
o	Return a JSON list of temperature observations for the previous year.
5.	/api/v1.0/<start> and /api/v1.0/<start>/<end>
o	Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
o	For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
o	For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
