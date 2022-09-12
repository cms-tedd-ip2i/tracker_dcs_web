from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import os
import tracker_dcs_web.web_server.data as data
from tracker_dcs_web.utils.logger import logger

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Tracker DCS Web Server for data ingestion",
    }


@app.post("/data", status_code=status.HTTP_201_CREATED)
async def upload_data(measurements: str):
    try:
        data.measurements.set(measurements)
    except ValueError as err:
        message = str(err)
        logger.warning(err)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=message
        )
    data.measurements.save()
    return data.measurements.to_list()


@app.post("/mapping", status_code=status.HTTP_201_CREATED)
async def post_mapping(mapping: str):
    try:
        data.mapping.set(mapping)
    except ValueError as err:
        message = str(err)
        logger.warning(err)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=message
        )
    data.mapping.save()
    return data.mapping.to_dict()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, access_log=False, timeout_keep_alive=60)
