# Climate Analysis with Flask Integration

### Introduction

This project involves the climate data analysis and creating a web-based interface using Flask to access the analyzed data. The analysis includes exploring precipitation data, station information, temperature data, and more.

### Data Analysis 

The Python script (climate.ipynb) performs data analysis and calculations on climate data, including precipitation and station analysis.

#### 1. Data Retrieval and Setup

- **Reflection and Setup**: The script sets up SQLAlchemy to reflect the tables in the database and establish a connection to the "hawaii.sqlite" database file. This is done using SQLAlchemy and automap.

- **Recent Date Retrieval**: It queries the database to find the most recent date in the dataset, which is used for subsequent date calculations.

#### 2. Precipitation Analysis

- **Date Calculation**: The script calculates the date one year from the last date in the dataset. This will be used to retrieve the last 12 months of precipitation data.

- **Precipitation Query**: A query is executed to retrieve precipitation data (date and prcp) for the last 12 months, starting from the calculated date.

- **Data to DataFrame**: The query results are saved in a Pandas DataFrame, and the columns are explicitly named.

- **Data Sorting**: The DataFrame is sorted by date.

- **Data Plotting**: The precipitation data is plotted using Matplotlib. The plot displays the relationship between date and precipitation.

- **Summary Statistics**: Using Pandas, summary statistics (mean, standard deviation, minimum, and maximum) are calculated for the precipitation data.

#### 3. Station Analysis

- **Station Count**: A query is executed to calculate the total number of stations in the dataset.

- **Most Active Stations**: A query is performed to find the most active stations by listing station names and their observation counts in descending order. The station with the highest number of observations is identified.

- **Temperature Analysis for Most Active Station**:
  - The most active station is identified based on the previous query.
  - Temperature statistics, including minimum, maximum, and average temperatures, are calculated for the identified most active station.

- **Temperature Observation (TOBS) Analysis for Most Active Station**:
  - The script queries the last 12 months of temperature observation data (TOBS) for the most active station.
  - The data is saved in a DataFrame and plotted as a histogram to display the temperature distribution.
  
#### 4. Session Closure

- The script ensures that the database session is closed to release resources.




### Flask Routes and Calculations

In the Flask application (app.py), various routes are defined to retrieve specific climate-related data. Here's a detailed explanation of each route and the calculations they perform:

#### 1. /api/v1.0/precipitation

- **Function**: This route provides precipitation data for the last year.

- **Calculations**:
  - The route calculates the date one year ago based on the most recent date in the climate data.
  - It queries the database to retrieve precipitation data for the last year, including date, precipitation (prcp), and station.
  - The data is returned as a JSON response, with dates as keys and precipitation data as values.

#### 2. /api/v1.0/stations

- **Function**: This route lists the available climate stations.

- **Calculations**:
  - The route queries the database to retrieve station information, including station IDs and names.
  - The station data is returned as a JSON response in a list of dictionaries.

#### 3. /api/v1.0/tobs

- **Function**: This route provides temperature observations for the most active station in the last year.

- **Calculations**:
  - The route determines the most active station based on the highest number of temperature observations.
  - It calculates the date one year ago for the most active station.
  - Temperature observations are queried for the last year, including date and temperature (tobs), for the most active station.
  - The temperature data is returned as a JSON response.

#### 4. /api/v1.0/<start> and /api/v1.0/<start>/<end>

- **Function**: These routes offer minimum, average, and maximum temperature statistics starting from the specified date (YYYY-MM-DD). The second route also allows specifying an end date.

- **Calculations**:
  - The routes query the database to calculate temperature statistics, including minimum (TMIN), average (TAVG), and maximum (TMAX) temperatures.
  - For the first route (/api/v1.0/<start>), the calculations start from the specified date and continue until the last available date in the database.
  - For the second route (/api/v1.0/<start>/<end>), the calculations are performed within the specified date range.
  - The resulting temperature statistics are returned as JSON responses.

The Flask application, when run, allows users to access these routes and retrieve climate-related data, making it a user-friendly interface for the climate analysis project.

#### Instructions

To run the project and access the data:

1. Ensure you have the required libraries and dependencies installed.
2. Run the Flask application using Python.

After running the application, you can visit the provided routes to access specific climate data.
