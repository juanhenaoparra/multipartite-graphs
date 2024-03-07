# app/api/endpoints/json_upload.py
from fastapi import APIRouter, File, UploadFile
from app.services import json_upload_service
from app.schemas import graphs as graph_schema
from app.controller import graphs as graph_controller
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.settings import get_db

router = APIRouter()

@router.post("/upload")
def upload(graph: graph_schema.GraphSchema, db: Session = Depends(get_db)):
    graph_create = graph_controller.create_graph(db=db, new_graph=graph)

    print(graph)
    response = graph_create
    return  response

@router.get("/graphs/{graph_name}", response_model=graph_schema.GraphSchema)
def get_graph_by_name(graph_name: str, db: Session = Depends(get_db)):
    return graph_controller.fetch_graph_by_name(db, graph_name)


@router.post("/upload/file")
async def upload_json(file: UploadFile = File(...)):
    return await json_upload_service.handle_json_upload(file)
