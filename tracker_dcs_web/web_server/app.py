from fastapi import FastAPI, status
import os
import tracker_dcs_web.web_server.data as data


app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Tracker DCS Web Server for data ingestion",
    }


@app.post("/data", status_code=status.HTTP_201_CREATED)
async def upload_data(measurements: data.Sensor):
    return measurements.data


@app.post("/mapping", status_code=status.HTTP_201_CREATED)
async def post_mapping(mapping: str):
    data.mapping.set(mapping)
    data.mapping.save()
    return data.mapping.to_dict()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, access_log=False, timeout_keep_alive=60)
