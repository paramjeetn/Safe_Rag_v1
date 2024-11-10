from fastapi import FastAPI, HTTPException, Depends, status
from dbos import DBOS
from typing import List, Dict
from sqlalchemy import select, and_
from pydantic import BaseModel
from .schema import file_status 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

allowed_origins = [
    "*",  # for local React development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # or use ["*"] for open access
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods
    allow_headers=["*"],  # allows all headers
)

DBOS(fastapi=app)


class FileStatusCreate(BaseModel):
    file_id: str
    file_etags: str
    added_by_user_id: str
    chrome_index_made: bool
    process_status: bool


class FileStatusRequest(BaseModel):
    file_ids: List[str]

# Add CORS middleware to your app



@app.post("/api/v1/check_file_status")
@DBOS.transaction()
def check_file_status(request: FileStatusRequest) -> Dict[str, bool]:
    """
    API to check the status of files based on file_ids provided.
    
    Returns a dictionary indicating whether each file has both chrome_index_made and process_status as True.
    """
    file_status_responses = {}

    for file_id in request.file_ids:
        # Check if the file_id exists in the database and get its status
        result = DBOS.sql_session.execute(
            select(file_status).filter(file_status.c.file_id == file_id)
        ).fetchone()

        if result:
            # If the file exists, check the status of chrome_index_made and process_status
            chrome_index_made = result.chrome_index_made
            process_status = result.process_status
            
            # Store True only if both statuses are True
            file_status_responses[file_id] = chrome_index_made and process_status
        else:
            # If the file does not exist, store False
            file_status_responses[file_id] = False

    # Return the response indicating the status of each file_id
    return file_status_responses








@app.post("/api/v1/save_file_status")
@DBOS.transaction()
def save_file_status(file_data: FileStatusCreate):
    try:
        DBOS.sql_session.execute(
            file_status.insert().values(
                file_id=file_data.file_id,
                file_etags=file_data.file_etags,
                added_by_user_id=file_data.added_by_user_id,
                chrome_index_made=file_data.chrome_index_made,
                process_status=file_data.process_status
            )
        )
        
        return {"status": "success"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file status: {str(e)}"
        )
