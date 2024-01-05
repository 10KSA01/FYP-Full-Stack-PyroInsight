from typing import List
import databases
import sqlalchemy
from sqlalchemy import select, func, and_, distinct, desc, text, cast, DateTime, or_
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

logger = logging.getLogger(__name__)

### to start server: "python -m uvicorn backend:app --reload" ###
## Don't press the play button in the top right corner, it will not work ##
user = "postgres"
password = "TestServer123"
tablename = "sim05-01-24"
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
    instantaneous_fault_state: int
    confirmed_fault_state: int
    acknowledged_fault_state: int

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

# Shows all the nodes in the database
@app.get("/all-nodes/", response_model=List[int])
async def get_all_nodes():
    query = select(distinct(data.c.node))
    result = await database.fetch_all(query)
    nodes = sorted([row[0] for row in result])
    return nodes

######### Devices #########
# Gets the all the information of a all devices into page sorted my datetime
@app.get("/device/page", response_model=List[Data], status_code=status.HTTP_200_OK)
async def get_all_device_page_data(request: Request, page: int = 0):
    # http://127.0.0.1:8000/device/page?2 (for page 2)
    items_per_page = 50
    skip = page * items_per_page
    take = items_per_page

    query = data.select().offset(skip).limit(take)
    result = await database.fetch_all(query)
    return result

# Gets the all the information of every device
@app.get("/device/all/", response_model=List[Data], status_code = status.HTTP_200_OK)
async def get_all_devices_data():
    query = data.select()
    return await database.fetch_all(query)

# Gets the all the information of a specific device
@app.get("/device/{id}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_device_data(id: str):
    query = data.select().where(data.c.id == id)
    result = await database.fetch_all(query)

    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

# Gets the latest the information of a specific device
@app.get("/device/{id}/latest/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def get_latest_device_data(id: str):
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

######### Panel #########
# Gets the all the information of a all the devices in a specific node/panel
@app.get("/panel/{node}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def get_panel_data(node: int):
    query = data.select().where(data.c.node == node)
    result = await database.fetch_all(query)
    print(result)
    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

# Gets the latest the information of a all the devices in a specific node/panel
@app.get("/panel/{node}/latest/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def get_latest_panel_data(node: int):
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

# Get all the disabled devices in a panel/node
@app.get("/panel/{node}/disabled/", status_code=status.HTTP_200_OK)
async def get_disabled_devices_panel(node: int):
    query = (
        select([func.count()])
        .where(data.c.node == node)
        .where(data.c.reply_status == "Failure")
    )

    result = await database.fetch_one(query)

    return result[0]

# Get the latest/current disabled devices in a panel/node
@app.get("/panel/{node}/disabled/latest", response_model=float, status_code=status.HTTP_200_OK)
async def get_latest_disabled_devices_panel(node: int):
    try:
        result = await query_data(node)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        # Count the number of faulty devices (reply_status == "Failure")
        faulty_devices = sum(1 for row in result if row["reply_status"] == "Failure")
        print(faulty_devices)
        return float(faulty_devices)
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

async def query_data(node: int):
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

# Get all the faulty devices in a panel/node
@app.get("/panel/{node}/faulty/", status_code=status.HTTP_200_OK)
async def count_fault(node: int):
    query = (
        select([func.count()])
        .where(data.c.node == node)
        .where(
            or_(
                data.c.instantaneous_fault_state > 0,
                data.c.confirmed_fault_state > 0,
                data.c.acknowledged_fault_state > 0
            )
        )
    )

    result = await database.fetch_one(query)

    return {"faulty_rows": result[0]}

# Get the latest/current faulty devices in a panel/node
@app.get("/panel/{node}/faulty/latest/", status_code=status.HTTP_200_OK)
async def count_latest_fault(node: int):
    latest_datetime_query = select([func.max(data.c.datetime)]).where(data.c.node == node)

    query = (
        select([func.count()])
        .where(data.c.node == node)
        .where(data.c.datetime == latest_datetime_query.as_scalar())
        .where(
            or_(
                data.c.instantaneous_fault_state > 0,
                data.c.confirmed_fault_state > 0,
                data.c.acknowledged_fault_state > 0
            )
        )
    )

    result = await database.fetch_one(query)

    return {"faulty_rows": result[0]}

# Get the average smoke/heat/co/dirtiness of all devices in a panel/node
@app.get("/panel/average/{type}/{node}/", response_model=float, status_code=status.HTTP_200_OK)
async def get_average_measurement(node: int, type: str):
    
    measure_columns = {
        "smoke": (data.c.units_of_measure1, data.c.converted_value1, "%/m obscuration"),
        "heat": (data.c.units_of_measure2, data.c.converted_value2, "Degrees C"),
        "co": (data.c.units_of_measure3, data.c.converted_value3, "ppm (parts per million)"),
        "dirtiness": (data.c.dirtiness, None, None)
    }

    if type not in measure_columns:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid type: {type}")

    unit_of_measure_column, value_of_measure_column, type_of_measure = measure_columns[type]

    try:
        query = (
            select([func.avg(value_of_measure_column).label('average')])
            .where(data.c.node == node)
            .where(unit_of_measure_column == type_of_measure)
        )

        result = await database.fetch_one(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return float(result['average'])
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

# Get the latest average smoke/heat/co/dirtiness of all devices in a panel/node    
@app.get("/panel/average/{type}/{node}/period/", response_model=List[Dict[str, Union[float, str]]], status_code=status.HTTP_200_OK)
async def get_average_measurement_period(node: int, type:str):
    # http://127.0.0.1:8000/panel/average/heat/0/period
    measure_columns = {
        "smoke": (data.c.units_of_measure1, data.c.converted_value1, "%/m obscuration"),
        "heat": (data.c.units_of_measure2, data.c.converted_value2, "Degrees C"),
        "co": (data.c.units_of_measure3, data.c.converted_value3, "ppm (parts per million)"),
        "dirtiness": (data.c.dirtiness, None, None)
    }

    if type not in measure_columns:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid type: {type}")

    unit_of_measure_column, value_of_measure_column, type_of_measure = measure_columns[type]
    try:
        # Get the timestamp of the first entry
        first_entry_query = select([data.c.datetime]).where(data.c.node == node).order_by(data.c.datetime).limit(1)
        first_entry_result = await database.fetch_one(first_entry_query)
        start_time = first_entry_result[0]  # assign the datetime directly

        # Get the current timestamp
        end_time = datetime.now()

        # Query for average heat over the time period
        if type == "dirtiness":
            query = (
                select([func.avg(data.c.dirtiness).label('average'), cast(func.to_timestamp(func.to_char(data.c.datetime, text("'YYYY-MM-DD HH24:MI'")), 'YYYY-MM-DD HH24:MI'), DateTime).label('formatted_datetime')])
                .where(data.c.node == node)
                .where(data.c.datetime >= start_time)
                .where(data.c.datetime <= end_time)
                .group_by(text("formatted_datetime"))
                .order_by(text("formatted_datetime"))
            )
        else:
            query = (
                select([func.avg(value_of_measure_column).label('average'), cast(func.to_timestamp(func.to_char(data.c.datetime, text("'YYYY-MM-DD HH24:MI'")), 'YYYY-MM-DD HH24:MI'), DateTime).label('formatted_datetime')])
                .where(data.c.node == node)
                .where(unit_of_measure_column == type_of_measure)
                .where(data.c.datetime >= start_time)
                .where(data.c.datetime <= end_time)
                .group_by(text("formatted_datetime"))
                .order_by(text("formatted_datetime"))
            )

        result = await database.fetch_all(query)

        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for the given node.")

        return [{type: float(r['average']), "datetime": str(r['formatted_datetime'])} for r in result]
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")