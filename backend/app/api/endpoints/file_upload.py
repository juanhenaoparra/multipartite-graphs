# app/api/endpoints/json_upload.py
from fastapi import APIRouter, File, UploadFile
from app.services import json_upload_service
from app.schemas import graphs as graph_schema
from app.schemas import bipartite as bipartite_schema
from app.schemas import generation as gen_schema
from app.controller import graphs as graph_controller
from app.controller import processes as process_controller
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.settings import get_db

router = APIRouter()


@router.post("/upload")
def upload(graph: graph_schema.GraphSchema, db: Session = Depends(get_db)):
    graph_create = graph_controller.create_graph(db=db, new_graph=graph)

    response = graph_create
    return  response

@router.get("/graphs/{graph_name}", response_model=graph_schema.GraphSchema)
def get_graph_by_name(graph_name: str, db: Session = Depends(get_db)):
    return graph_controller.fetch_graph_by_name(db, graph_name)

@router.post("/upload/file")
async def upload_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    processed_json = await json_upload_service.handle_json_upload(file)
    if "error" in processed_json:
        return processed_json
    else:
        # Llamar al método upload con el JSON procesado
        graph_data = processed_json
        graph_schema_obj = graph_schema.GraphSchema(**graph_data)
        graph_create = graph_controller.create_graph(db=db, new_graph=graph_schema_obj)

        response = graph_create
        return response

@router.post("/new", response_model=graph_schema.GraphSchema)
async def create_random_graph(graph_input: gen_schema.GenGraphInput, db: Session = Depends(get_db)):
    return graph_controller.create_random_graph(db, graph_input)

@router.get("/bipartite/{graph_name}", response_model=bipartite_schema.BipartiteMatchResponse)
async def check_bipartiteness(graph_name: str, db: Session = Depends(get_db)):
    return process_controller.check_bipartiteness(db, graph_name)

# Calculate minimum partition using dynamic programming
@router.post("/bipartite/minimum-partition/e1")
async def calculate_partition_distance(partition_input: bipartite_schema.SystemPartitionInput, db: Session = Depends(get_db)):
    return process_controller.calculate_partition_distance(
        db=db,
        full_system=partition_input.full_system,
        binary_distribution=partition_input.binary_distribution,
        subsystem=partition_input.subsystem,
    )

# Calculate minimum partition using edge removal with local search
@router.post("/bipartite/minimum-partition/e2")
async def calculate_partition_distance_v2(partition_input: bipartite_schema.SystemPartitionInput, db: Session = Depends(get_db)):
    return process_controller.calculate_edges_cut_distance(
        db=db,
        full_system=partition_input.full_system,
        binary_distribution=partition_input.binary_distribution,
        subsystem=partition_input.subsystem,
    )

# Calculate minimum partition using algorithm inspired in Ant Colony Optimization (ACO)
@router.post("/bipartite/minimum-partition/e3")
async def calculate_partition_distance_v3(partition_input: bipartite_schema.SystemPartitionInput, db: Session = Depends(get_db)):
    return process_controller.calculate_min_cut_with_aco(
        db=db,
        full_system=partition_input.full_system,
        binary_distribution=partition_input.binary_distribution,
        subsystem=partition_input.subsystem,
    )