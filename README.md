[![codecov](https://codecov.io/gh/cms-tedd-ip2i/tracker_dcs_web/branch/dev/graph/badge.svg?token=J1O1816LJK)](https://codecov.io/gh/cms-tedd-ip2i/tracker_dcs_web)

# Tracker DCS Web Server 

Input from outside, e.g. LabView

## Developer instructions

Environment creation: 

```
python -m venv venv
source venv/bin/activate
```

Installation: 

```
pip install --upgrade pip
pip install -r requirements/local.txt
pip install -e .  
```

## Environment variables 

| Variable        | Description     | Mandatory | Default   | 
|-----------------|-----------------|-----------|-----------| 
| MQTT_HOST       | mosquitto host  | no        | localhost | 
| MQTT_PORT       | mosquitto port  | no        | 1883      | 
| MQTT_TOPIC_DATA | mqtt root topic | no        | /labview  |

## Docker stack 

To run the unit tests on the web server locally you need an MQTT broker. Start it: 

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
curl localhost:8001/
```




