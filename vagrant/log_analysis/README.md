# Log Analysis Project
The Log Analysis script queries the news database to answer the following questions:
    
    1. What are the most popular three articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of requests lead to errors?

The script uses one query per question to select the answer.

## Installation
In order to run the script make sure to install `psycopg2` using the following command:

`$ pip install psycopg2`

## Usage
To run the Log Analysis script `cd` to the directory where they script is saved and then run the following command:

`$ python log_analysis.py`