# cc-api

This project is a simple currency convertor API .


## Assumptions

* I assumed there will be no need to manage currency_from, currency_to, date pairs i.e making this tuple of information unique such that there will only be one instance of such data at any point in time.

* I also assumed user may want to query database on multiple parameters hence that provision was made.

* I allowed for uses to create multiple currency conversion pairs and did not limit myself to the once in the csv


## Initial Project Setup
It is assumed that you are familiar with docker and have docker setup on your development machine.  
In case you have not done this, or are unfamilair with docker,  
kindly visit [docker getting started](https://docs.docker.com/get-started/)

Once done setting up docker, clone the code.  
Navigate to the cc-api directory.  
In case you don't know how to get this done speak to someone on the project who can help.

**NB//** This is for local development
Run the command below in order to get started:

## Steps To Run:

A.
    Builds and starts an instance of the image

    1. > $ docker compose  up -d
    
    2. > $ docker exec -it cc-api_app_1 /bin/bash

    3. > $ uvicorn app.main:app --host 0.0.0.0 --port 8080


B. Run Migrations

    1. > $ docker compose  up -d
    
    2. > $ docker exec -it cc-api_app_1 /bin/bash

    3. > $ alembic upgrade head

C. Import Data

    1. > $ docker compose  up -d
    
    2. > $ docker exec -it cc-api_app_1 /bin/bash

    3. > $ cd data/

    4. > $ python import.py


## Improvements

* Swicth to Postgres

* Add Unit tests

* Add more comments and better API documentation

## TO DO
5. Implement endpoint that calculate rate for given currency pair at given date. In case there is no such currency pair, you need to calculate it by using others, for example for input NZD/AUD you can calculate rate by converting NZD -> USD -> AUD. If there are couple of variations we need minimal rate.






## How to access server

* Server is accessible at [http://localhost:8080/](http://localhost:8080/)

* Swagger Documentation can be found here [http://localhost:8080/docs/](http://localhost:8080/docs/)

* Alternative Documentation can be found here [http://localhost:8080/redoc/](http://localhost:8080/redoc/)