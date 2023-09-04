from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.logger import logger as fastapi_logger
import logging
from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

API_KEY = os.environ.get('KEY')
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Enabling logging in docker container
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.handlers = gunicorn_error_logger.handlers
if __name__ != "__main__":
    fastapi_logger.setLevel(gunicorn_logger.level)
else:
    fastapi_logger.setLevel(logging.DEBUG)


class RowsRequest(BaseModel):
    rows_amount: int


# setting the api key
def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


async def makerows(rows):
    row_number = 1
    rowlist = {'rows':[]}
    for x in range(rows):
        rowlist['rows'].append({'row': row_number}) 
        row_number += 1
    return rowlist


@app.post('/rows')
async def rows_api(data: RowsRequest, api_key: str = Security(get_api_key)):
    response = makerows(data.rows_amount)
    try:
        return await response
    except Exception as e:
        return JSONResponse(status_code=500, content={'reason': str(e)})