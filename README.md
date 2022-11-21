[![codecov](https://codecov.io/gh/cms-tedd-ip2i/tracker_dcs_web/branch/dev/graph/badge.svg?token=J1O1816LJK)](https://codecov.io/gh/cms-tedd-ip2i/tracker_dcs_web)

# Tracker DCS Web Server 

Input from outside, e.g. LabView

## Developer instructions

Local installation: 

```
conda create -n web_server python=3.9
conda activate web_server
pip install --upgrade pip
pip install -r requirements/local.txt
pip install -e .  
```

## Environment variables 

These secrets will be printed out by the server. 
They are not used for authentication, so set them to whatever you want. 

* `APP_USER`: app user
* `APP_PASSWORD`: app password
* `MQTT_HOST`: mosquitto host, e.g. localhost (don't include the port)

## Docker stack 

To run the unit tests you need an MQTT broker. Start it: 

```commandline
cd docker/test_tracker_dcs_web
docker-compose up -d 
```

## Unit tests and linting 

Black: 

```commandline
black . --exclude _actions
```

Unit tests: 

```commandline
cd unittests
pytest
```

## Running locally

```
python web_server/app.py
```

Visit the API docs page to try the endpoints:
[http://localhost:5000/docs](http://localhost:5000/docs)

The root endpoint will print the secrets you have set. 

You can also try the other endpoints. 

## Running in docker

See the docker-compose stack, the web_server is already integrated. 

To make a request to the root path: 

```commandline
curl curl localhost:8001/
```




