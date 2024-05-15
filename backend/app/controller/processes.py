from fastapi import HTTPException

import ast
from sqlalchemy.orm import Session
from app.schemas.graphs import GraphSchema
from ..models import graph as graph_model
from ..services.matching import CheckBipartite, NotBipartiteException, BipartiteMatchResponse
from ..services.compare_partitions import calculate_minimum_partition

def check_bipartiteness(db: Session, graph_name: str) -> BipartiteMatchResponse:
    graph = db.query(graph_model.Graph).filter(graph_model.Graph.name == graph_name).first()

    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")

    graph_sch = GraphSchema(name=graph.name, data=ast.literal_eval(graph.data))

    try:
        chk = CheckBipartite(graph_sch)

        res = chk.process()

        return res
    except NotBipartiteException as e:
        return BipartiteMatchResponse(isBipartite=False, reason=str(e))
    finally:
        graph.data = str(graph_sch.model_dump()["data"])

        db.commit()
        db.refresh(graph)

def calculate_partition_distance(db: Session, full_system, matrix, binary_distribution) -> float:
    return calculate_minimum_partition(
        full_system=full_system,
        matrix=matrix,
        binary_distribution=binary_distribution,
    )