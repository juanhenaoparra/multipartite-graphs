import datetime
from fastapi import HTTPException

import ast
from sqlalchemy.orm import Session
from app.schemas.graphs import GraphSchema
from ..models import graph as graph_model
from ..services.matching import CheckBipartite, NotBipartiteException, BipartiteMatchResponse
from ..services.compare_partitions import calculate_minimum_partition
from ..services.edges_cut_removal import calculate_edges_cut

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
    start_date = datetime.datetime.now()

    res = calculate_minimum_partition(
        full_system=full_system,
        matrix=matrix,
        binary_distribution=binary_distribution,
    )

    res.stats["elapsed_time_secs"] = (datetime.datetime.now() - start_date).total_seconds()

    return res

def calculate_edges_cut_distance(db: Session, full_system, matrix, binary_distribution) -> float:
    start_date = datetime.datetime.now()

    res = calculate_edges_cut(
        p_matrix=full_system,
        binary_distribution=binary_distribution,
        futureNodesCount=len(matrix[0]),
        presentNodesCount=len(matrix[1]),
        base_effect=tuple(matrix[0]),
        base_cause=tuple(matrix[1]),
    )

    res.stats["elapsed_time_secs"] = (datetime.datetime.now() - start_date).total_seconds()

    return res