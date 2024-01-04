from typing import List
import databases
import sqlalchemy
from sqlalchemy import select, func, and_, distinct, desc, text
from fastapi import FastAPI, status, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse
import pandas as pd
from fastapi import HTTPException
import logging
import traceback
from typing import Dict, Union, List
from sqlalchemy import text

logger = logging.getLogger(__name__)

### to start server: "python -m uvicorn backend:app --reload" ###
## Don't press the play button in the top right corner, it will not work ##
user = "postgres"
password = "TestServer123"
tablename = "sim01-01-24"
host = "localhost"
port = "5432"
dbname = "Devices"
# sslmode = "require"

# DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode={sslmode}"
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

engine = sqlalchemy.create_engine(DATABASE_URL)

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

# Assuming you have an existing table main in the database
data = sqlalchemy.Table(
    tablename,
    metadata,
    autoload=True,  # This line loads the existing table definition
    autoload_with=engine,
)

metadata.create_all(engine)

class Data(BaseModel):
    id: str
    datetime: datetime
    reply_status: str
    node: int
    channel_address: int
    point_number: int
    logical_point_number: int
    logical_point_zone: int
    device_type: str
    dirtiness: int
    units_of_measure1: str
    units_of_measure2: str
    units_of_measure3: str
    converted_value1: int
    converted_value2: int
    converted_value3: int


app = FastAPI(title = "REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/all_device", response_model=List[Data], status_code = status.HTTP_200_OK)
async def read_data():
    query = data.select()
    return await database.fetch_all(query)

@app.get("/data/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_data(request: Request, page: int = 0):
    items_per_page = 50
    skip = page * items_per_page
    take = items_per_page

    query = data.select().offset(skip).limit(take)
    result = await database.fetch_all(query)
    return result

@app.get("/device/{id}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_device_data(id: str):
    query = data.select().where(data.c.id == id)
    result = await database.fetch_all(query)

    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

@app.get("/device/{id}/latest", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_latest_device_data(id: str):
    subquery = (
        select([func.max(data.c.datetime).label("latest_datetime")])
        .where(data.c.id == id)
    ).alias("latest_subquery")
    
    query = (
        select([data])
        .where(data.c.id == id)
        .where(data.c.datetime == subquery.c.latest_datetime)
    ).order_by(desc(data.c.datetime))
    
    result = await database.fetch_all(query)

    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

@app.get("/panel/{node}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_panel_data(node: int):
    query = data.select().where(data.c.node == node)
    result = await database.fetch_all(query)

    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

@app.get("/latest-panel/{node}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_latest_panel_data(node: int):
    try:
        subquery = (
            select([data.c.node, data.c.id, func.max(data.c.datetime).label("latest_datetime")])
            .where(data.c.node == node)
            .group_by(data.c.node, data.c.id)
        ).alias("latest_subquery")

        query = (
            select([data])
            .select_from(data.join(subquery, and_(
                data.c.node == subquery.c.node,
                data.c.id == subquery.c.id,
                data.c.datetime == subquery.c.latest_datetime
            )))
            .order_by(data.c.id)
        )

        result = await database.fetch_all(query)

        if not result:
            return JSONResponse(content={"message": "No data found for the given node."}, status_code=status.HTTP_404_NOT_FOUND)
        return result
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"message": "Internal server error."}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Shows all the nodes in the database
@app.get("/nodes", response_model=List[int])
async def get_nodes():
    query = select(distinct(data.c.node))
    result = await database.fetch_all(query)
    nodes = sorted([row[0] for row in result])
    return nodes


@app.get("/failure/{node}/", response_model=int, status_code=status.HTTP_200_OK)
async def read_latest_data(node: int):
    try:
        result = await fetch_data(node)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        # Count the number of faulty devices (reply_status == "Failure")
        faulty_devices = sum(1 for row in result if row["reply_status"] == "Failure")
        
        return faulty_devices
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

async def fetch_data(node: int):
    subquery = (
        select([data.c.node, data.c.id, func.max(data.c.datetime).label("latest_datetime")])
        .where(data.c.node == node)
        .group_by(data.c.node, data.c.id)
    ).alias("latest_subquery")

    query = (
        select([data])
        .select_from(data.join(subquery, and_(
            data.c.node == subquery.c.node,
            data.c.id == subquery.c.id,
            data.c.datetime == subquery.c.latest_datetime
        )))
        .order_by(data.c.id)
    )

    return await database.fetch_all(query)

# Smoke - %/m obscuration
@app.get("/average-obscuration/{node}/", response_model=float, status_code=status.HTTP_200_OK)
async def get_average_obscuration(node: int):
    try:
        query = (
            select([func.avg(data.c.converted_value1).label('average')])
            .where(data.c.node == node)
            .where(data.c.units_of_measure1 == "%/m obscuration")
        )

        result = await database.fetch_one(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return float(result['average'])
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@app.get("/average-obscuration-period/{node}/", response_model=List[Dict[str, Union[float, str]]], status_code=status.HTTP_200_OK)
async def get_average_obscuration_period(node: int):
    try:
        # Get the timestamp of the first entry
        first_entry_query = select([data.c.datetime]).where(data.c.node == node).order_by(data.c.datetime).limit(1)
        first_entry_result = await database.fetch_one(first_entry_query)
        start_time = first_entry_result[0]  # assign the datetime directly

        # Get the current timestamp
        end_time = datetime.now()

        # Query for average obscuration over the time period
        query = (
            select([func.avg(data.c.converted_value1).label('average'), func.to_char(data.c.datetime, text("'Dy Mon DD HH24:MI YYYY'")).label('formatted_datetime')])
            .where(data.c.node == node)
            .where(data.c.units_of_measure1 == "%/m obscuration")
            .where(data.c.datetime >= start_time)
            .where(data.c.datetime <= end_time)
            .group_by(text("formatted_datetime"))
            .order_by(text("formatted_datetime"))
        )

        result = await database.fetch_all(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return [{"obscuration": float(r['average']), "datetime": str(r['formatted_datetime'])} for r in result]
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

# Heat - Degrees C
@app.get("/average-heat/{node}/", response_model=float, status_code=status.HTTP_200_OK)
async def get_average_heat(node: int):
    try:
        query = (
            select([func.avg(data.c.converted_value2).label('average')])
            .where(data.c.node == node)
            .where(data.c.units_of_measure2 == "Degrees C")
        )

        result = await database.fetch_one(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return float(result['average'])
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@app.get("/average-heat-period/{node}/", response_model=List[Dict[str, Union[float, str]]], status_code=status.HTTP_200_OK)
async def get_average_heat_period(node: int):
    try:
        # Get the timestamp of the first entry
        first_entry_query = select([data.c.datetime]).where(data.c.node == node).order_by(data.c.datetime).limit(1)
        first_entry_result = await database.fetch_one(first_entry_query)
        start_time = first_entry_result[0]  # assign the datetime directly

        # Get the current timestamp
        end_time = datetime.now()

        # Query for average heat over the time period
        query = (
            select([func.avg(data.c.converted_value2).label('average'), func.to_char(data.c.datetime, text("'Dy Mon DD HH24:MI YYYY'")).label('formatted_datetime')])
            .where(data.c.node == node)
            .where(data.c.units_of_measure2 == "Degrees C")
            .where(data.c.datetime >= start_time)
            .where(data.c.datetime <= end_time)
            .group_by(text("formatted_datetime"))
            .order_by(text("formatted_datetime"))
        )

        result = await database.fetch_all(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return [{"heat": float(r['average']), "datetime": str(r['formatted_datetime'])} for r in result]
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

# CO - ppm (parts per million)
@app.get("/average-co/{node}/", response_model=float, status_code=status.HTTP_200_OK)
async def get_average_co(node: int):
    try:
        query = (
            select([func.avg(data.c.converted_value3).label('average')])
            .where(data.c.node == node)
            .where(data.c.units_of_measure3 == "ppm (parts per million)")
        )

        result = await database.fetch_one(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return float(result['average'])
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@app.get("/average_co-period/{node}/", response_model=List[Dict[str, Union[float, str]]], status_code=status.HTTP_200_OK)
async def get_average_co_period(node: int):
    try:
        # Get the timestamp of the first entry
        first_entry_query = select([data.c.datetime]).where(data.c.node == node).order_by(data.c.datetime).limit(1)
        first_entry_result = await database.fetch_one(first_entry_query)
        start_time = first_entry_result[0]  # assign the datetime directly

        # Get the current timestamp
        end_time = datetime.now()

        # Query for average heat over the time period
        query = (
            select([func.avg(data.c.converted_value3).label('average'), func.to_char(data.c.datetime, text("'Dy Mon DD HH24:MI YYYY'")).label('formatted_datetime')])
            .where(data.c.node == node)
            .where(data.c.units_of_measure3 == "ppm (parts per million)")
            .where(data.c.datetime >= start_time)
            .where(data.c.datetime <= end_time)
            .group_by(text("formatted_datetime"))
            .order_by(text("formatted_datetime"))
        )

        result = await database.fetch_all(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return [{"co": float(r['average']), "datetime": str(r['formatted_datetime'])} for r in result]
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


