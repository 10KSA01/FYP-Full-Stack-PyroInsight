from typing import List
import databases
import sqlalchemy
from sqlalchemy import select, func, and_, distinct, desc
from fastapi import FastAPI, status, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse
import pandas as pd

### to start server: "python -m uvicorn backend:app --reload" ###
## Don't press the play button in the top right corner, it will not work ##
user = "jacharku"
password = "TestServer123"
tablename = "sqa13-09-23"
host = "test-jacharku.postgres.database.azure.com"
port = "5432"
dbname = "testing"
sslmode = "require"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode={sslmode}"

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
async def read_data(id: str):
    query = data.select().where(data.c.id == id)
    result = await database.fetch_all(query)

    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

@app.get("/device/{id}/latest", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_latest_data(id: str):
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
async def read_data(node: int):
    query = data.select().where(data.c.node == node)
    result = await database.fetch_all(query)

    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

@app.get("/latest-panel/{node}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_latest_data(node: int):
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

# Returns how many devices in a node where the replay status is "Failure"
@app.get("/failure/{node}/", response_model=int, status_code=status.HTTP_200_OK)
async def read_latest_data(node: int):
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

        # Count the number of faulty devices (reply_status == "Failure")
        faulty_devices = sum(1 for row in result if row["reply_status"] == "Failure")
        
        return faulty_devices
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"message": "Internal server error."}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


