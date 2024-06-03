import datetime
from fastapi import HTTPException
import ast
from sqlalchemy.orm import Session
import numpy as np
import math

from app.schemas.graphs import GraphSchema
from ..models import graph as graph_model
from ..services.matching import CheckBipartite, NotBipartiteException, BipartiteMatchResponse
from ..services.compare_partitions import calculate_minimum_partition
from ..services.edges_cut_removal import calculate_edges_cut
from ..services.matrix import get_subsystem_distribution

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

def calculate_partition_distance(db: Session, full_system, binary_distribution, subsystem) -> float:
    start_date = datetime.datetime.now()
    full_system = np.array(full_system)

    if subsystem is not None:
        full_system = get_subsystem_distribution(matrix=full_system, axis=1, effect=tuple(subsystem[0]), cause=tuple(subsystem[1]))
        binary_distribution = "".join([binary_distribution[i] for i in subsystem[1]])

    res = calculate_minimum_partition(
        full_system=full_system,
        binary_distribution=binary_distribution,
    )

    res.stats["elapsed_time_secs"] = (datetime.datetime.now() - start_date).total_seconds()

    return res

def calculate_edges_cut_distance(db: Session, full_system, binary_distribution, subsystem) -> float:
    start_date = datetime.datetime.now()
    full_system = np.array(full_system)

    if subsystem is not None:
        full_system = get_subsystem_distribution(matrix=full_system, axis=1, effect=tuple(subsystem[0]), cause=tuple(subsystem[1]))
        binary_distribution = "".join([binary_distribution[i] for i in subsystem[1]])

    system_shape_rows, system_shape_columns = full_system.shape

    effects_size = round(system_shape_columns/2)
    causes_size = round(math.log2(system_shape_rows))

    res = calculate_edges_cut(
        p_matrix=full_system,
        binary_distribution=binary_distribution,
        futureNodesCount=effects_size,
        presentNodesCount=causes_size,
        base_effect=tuple(range(effects_size)),
        base_cause=tuple(range(causes_size)),
    )

    res.stats["elapsed_time_secs"] = (datetime.datetime.now() - start_date).total_seconds()

    return res