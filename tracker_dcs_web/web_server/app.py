import json

from fastapi import FastAPI, status, File, UploadFile
from fastapi.responses import JSONResponse
import os
import tracker_dcs_web.web_server.data as data
from tracker_dcs_web.utils.logger import logger
from tracker_dcs_web.mqtt import client

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Tracker DCS Web Server for data ingestion",
    }


@app.post("/data", status_code=status.HTTP_201_CREATED)
async def upload_data(measurements: str):
    logger.info(f"/data {measurements}")
    try:
        data.measurements.set(measurements)
    except ValueError as err:
        message = str(err)
        logger.warning(err)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=message
        )
    records = data.measurements.records()
    if records:
        mqtt_topic = os.environ.get("MQTT_TOPIC_DATA", "/labview")
        logger.info(f"publishing {records}")
        client.publish(mqtt_topic, json.dumps(records), qos=2)
        data.measurements.clear()
        return records
    else:
        return data.measurements.columns()


@app.post(
    "/mapping",
    status_code=status.HTTP_201_CREATED,
)
async def post_mapping(upload_file: UploadFile = File(...)):
    mapping = upload_file.file.read().decode("utf8")
    logger.debug("set mapping")
    logger.debug(mapping)
    try:
        data.mapping.set(mapping)
    except ValueError as err:
        message = str(err)
        logger.warning(err)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=message
        )
    return data.mapping.to_dict()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, access_log=False, timeout_keep_alive=60)
