from fastapi import FastAPI
import os

from datetime import datetime, timezone


app = FastAPI()


@app.get("/api")
async def null_item():
    converted_date = datetime.now().replace(tzinfo=timezone.utc)
    unix_var = datetime.timestamp(converted_date)

    return {
        "unix": int(unix_var * 1000),
        "utc": converted_date.strftime("%a, %d %b %Y, %H:%M:%S %Z"),
    }


@app.get("/api/{raw_date}")
async def read_item(raw_date: str):
    try:
        unix_var = int(raw_date) // 1000
        print(unix_var)
        converted_date = datetime.fromtimestamp(unix_var).replace(tzinfo=timezone.utc)
        print(converted_date)
    except ValueError:
        try:
            converted_date = datetime.strptime(raw_date, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            unix_var = datetime.timestamp(converted_date)
        except ValueError:
            return {"error": "Invalid Date"}

    return {
        "unix": int(unix_var * 1000),
        "utc": converted_date.strftime("%a, %d %b %Y, %H:%M:%S %Z"),
    }


@app.get("/health")
async def health_check():
    # return the current valaue of GIT_SHA
    return {"version": os.getenv("GIT_SHA"), "build_timestamp": os.getenv("BUILD_DATE")}
