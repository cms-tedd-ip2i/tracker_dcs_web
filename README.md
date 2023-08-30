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
pip install -e .[local]  
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
docker compose up -d 
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

To be written

## Injecting data 

* Start the DCS stack
* Go to the root of this package and then do:

```
export DATADIR=${PWD}/unittests/data/labview
dummy_labview http://localhost:8001 ${DATADIR}/mapping.txt ${DATADIR}/header.txt ${DATADIR}/measures.txt -n 10 
```

* Make sure you get mqtt messages : 

```
docker exec stack-mosquitto-1 mosquitto_sub -v -t /labview
```

```
/labview {"0 (PS)": 23.794608, "2 (PS)": 24.270239, "3 (PS)": 24.368866, "7 (PS)": 24.584218, "8 (PS)": 25.116412, "9 (PS)": 25.1832, "10 (PS)": 25.10516, "11 (PS)": 25.095721, "14 (PS)": 23.724818, "15 (PS)": 25.148199, "20 (PS)": 24.442453, "21 (PS)": 24.837407, "23 (PS)": 25.257441, "24 (PS)": 25.285556, "28 (PS)": 24.313686, "30 (PS)": 25.762269, "31 (PS)": 24.577083, "1 (2S)": 25.372097, "26 (2S)": 24.423724, "33 (2S)": 24.756658, "35 (2S)": 24.558114, "36 (2S)": 25.237437, "37 (2S)": 24.666911, "38 (2S)": 24.866404, "39 (2S)": 23.705506, "40 (2S)": 24.590622, "41 (2S)": 24.929428, "42 (2S)": 24.592504, "43 (2S)": 24.361401, "44 (2S)": 24.615935, "45 (2S)": 24.23221, "46 (2S)": 24.932867, "47 (2S)": 24.36999, "48 (2S)": 24.945494, "49 (2S)": 25.058509, "50 (2S)": 24.389153, "51 (2S)": 24.32974, "52 (2S)": 24.72595, "53 (2S)": 24.368981, "54 (2S)": 24.427689, "55 (2S)": 24.955819, "56 (2S)": 24.954875, "57 (2S)": 24.435747, "58 (2S)": 24.459637, "59 (2S)": 25.145329, "60 (2S)": 23.671368, "63 (2S)": 24.625984, "64 (2S)": 25.448417, "69": 27.223336, "70": 18.907616, "117": 28.239884, "118": 28.324767, "119": 28.506608, "1_T [oC]": 26.204834, "1_Igro. [%]": 0.905784, "1_Tr [oC]": -35.269409, "1_Tg [oC]": -32.027641, "1_M [Mol/l]": 303.450836, "2_T [oC]": 26.095947, "2_Igro. [%]": 0.919002, "2_Tr [oC]": -35.186695, "2_Tg [oC]": -31.950109, "2_M [Mol/l]": 305.948853, "PS [V]": -6.534825e-05, "2S [V]": 0.000188, "P [mbar]": 58.099059, "Datetime_ns": 1652951192000000000}
/labview {"0 (PS)": 23.474371, "2 (PS)": 23.844079, "3 (PS)": 24.138962, "7 (PS)": 24.540439, "8 (PS)": 25.033106, "9 (PS)": 25.019948, "10 (PS)": 25.038958, "11 (PS)": 25.047888, "14 (PS)": 23.451034, "15 (PS)": 25.107758, "20 (PS)": 24.051482, "21 (PS)": 24.631699, "23 (PS)": 25.223314, "24 (PS)": 25.217837, "28 (PS)": 24.071647, "30 (PS)": 25.693499, "31 (PS)": 24.337925, "1 (2S)": 25.32945, "26 (2S)": 24.360936, "33 (2S)": 24.698105, "35 (2S)": 24.508007, "36 (2S)": 25.183981, "37 (2S)": 24.609425, "38 (2S)": 24.818768, "39 (2S)": 23.707785, "40 (2S)": 24.538172, "41 (2S)": 24.873097, "42 (2S)": 24.553522, "43 (2S)": 24.329078, "44 (2S)": 24.561973, "45 (2S)": 24.098901, "46 (2S)": 24.896844, "47 (2S)": 24.317725, "48 (2S)": 24.901188, "49 (2S)": 24.994155, "50 (2S)": 24.246465, "51 (2S)": 24.182257, "52 (2S)": 24.664652, "53 (2S)": 24.381589, "54 (2S)": 24.392611, "55 (2S)": 24.893014, "56 (2S)": 24.911699, "57 (2S)": 24.422063, "58 (2S)": 24.422109, "59 (2S)": 25.082687, "60 (2S)": 23.696626, "63 (2S)": 24.579633, "64 (2S)": 25.405447, "69": 27.104352, "70": 19.102592, "117": 28.122215, "118": 28.217106, "119": 28.426495, "1_T [oC]": 26.12793, "1_Igro. [%]": 0.919471, "1_Tr [oC]": -35.162464, "1_Tg [oC]": -31.927399, "1_M [Mol/l]": 306.684235, "2_T [oC]": 26.030273, "2_Igro. [%]": 0.932644, "2_Tr [oC]": -35.077103, "2_Tg [oC]": -31.847408, "2_M [Mol/l]": 309.287231, "PS [V]": 0.000281, "2S [V]": -4.769084e-05, "P [mbar]": 58.309803, "Datetime_ns": 1652951202000000000}
```

