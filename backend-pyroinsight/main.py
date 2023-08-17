from typing import List
import databases
import sqlalchemy
from sqlalchemy import select, func, and_
from fastapi import FastAPI, status, Request, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse
import pandas as pd

### to start server: python -m uvicorn main:app --reload ###
## Don't press the play button in the top right corner, it will not work ##
user = "jacharku"
password = "TestServer123"
tablename = "t08-08-23"
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

# @app.get("/get_all_device", response_model=List[Data], status_code = status.HTTP_200_OK)
# async def read_data():
#     query = data.select()
#     fetch = await database.fetch_all(query)
#     df = pd.DataFrame(fetch)
#     print(df)

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

@app.get("/panel/{node}/", response_model=List[Data], status_code=status.HTTP_200_OK)
async def read_data(node: int):
    query = data.select().where(data.c.node == node)
    result = await database.fetch_all(query)
    
    if not result:
        return JSONResponse(content={"message": "No data found for the given id."}, status_code=status.HTTP_404_NOT_FOUND)

    return result

# @app.get("/latest-panel/{node}/", response_model=Data, status_code=status.HTTP_200_OK)
# async def read_latest_data(node: int):
#     # Subquery to find the latest datetime for each unique device within the node
#     subquery = (
#         select([data.c.node, data.c.device_type, func.max(data.c.datetime).label("latest_datetime")])
#         .where(data.c.node == node)
#         .group_by(data.c.node, data.c.device_type)
#         .alias("latest_datetime_subquery")
#     )

#     # Query to join the original table with the subquery to retrieve the latest data
#     query = (
#         select([data])
#         .select_from(data.join(subquery, (data.c.node == subquery.c.node) & (data.c.device_type == subquery.c.device_type)))
#         .where(data.c.datetime == subquery.c.latest_datetime)
#     )
    
#     result = await database.fetch_all(query)
    
#     if not result:
#         return JSONResponse(content={"message": "No data found for the given node."}, status_code=status.HTTP_404_NOT_FOUND)

#     return result


# @app.get("/latest-panel/{node}/", response_model=List[Data], status_code=status.HTTP_200_OK)
# async def read_latest_data(node: int):
#     # Query to select the latest datetime for each unique device within the specified node
#     query = (
#         select([data.c.node, data.c.id, func.max(data.c.datetime).label("latest_datetime")])
#         .where(data.c.node == node)
#         .group_by(data.c.node, data.c.id)
#     )
    
#     result = await database.fetch_all(query)
    
#     if not result:
#         return JSONResponse(content={"message": "No data found for the given node."}, status_code=status.HTTP_404_NOT_FOUND)

#     return result

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
        )
        
        result = await database.fetch_all(query)
        
        if not result:
            return JSONResponse(content={"message": "No data found for the given node."}, status_code=status.HTTP_404_NOT_FOUND)

        return result
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"message": "Internal server error."}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



