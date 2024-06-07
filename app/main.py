from fastapi import FastAPI
import os

from datetime import datetime, timezone


app = FastAPI()

@app.get("/api")
async def null_item():
    
    converted_date = datetime.now().replace(tzinfo= timezone.utc)
    unix_var = datetime.timestamp(converted_date)

    return {"unix": int(unix_var*1000), "utc": converted_date.strftime('%a, %d %b %Y, %H:%M:%S %Z')}

@app.get("/api/{raw_date}")
async def read_item(raw_date: str):

    try: 
        converted_date = datetime.strptime(raw_date,'%Y-%m-%d').replace(tzinfo= timezone.utc)
    except(ValueError):
        return {"error": "Invalid Date"}
    
    unix_var = datetime.timestamp(converted_date)

    return {"unix": int(unix_var*1000), "utc": converted_date.strftime('%a, %d %b %Y, %H:%M:%S %Z')}

@app.get("/health")
async def health_check():

    #return the current valaue of GIT_SHA
    return {"version": os.getenv("GIT_SHA")}