# Project currency converter

This is a simple currency converter written in Python 3.6.

Requisites:

- Python 3.6
- pip
- Flask framework
- xmltodict pip module
- flask_session pip module

Steps for running this application:

- install Python
- install pip
- install virtualenv
    sudo pip3 install virtualenv (in Linux environment)
- create application environment
    virtualenv convert_currencies
- install Flask framework
    pip install Flask
- change environment to convert_currencies development environment
    source bin/activate
- install xmltodict from pip
    sudo pip install xmltodict
- install flask_session from pip
    sudo pip install flask_session
- export environment variable FLASK_APP
    export FLASK_APP=application.py
- launch Flask framework
    flask run

At this point, we can send our requests via GET method convert:

- open a browser (or equivalent, via wget or curl)
- write the request with your desired parameters:
    http://localhost:5000/convert/<amount>/<source_currency>/<destination_currency>/<reference_date>

    for example:

    http://localhost:5000/convert/3.00/EUR/GBP/2019-01-24


Important: exchange rates are dinamically loaded every project startup (flask run) and are stored in Flask sessions
