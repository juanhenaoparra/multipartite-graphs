from typing import Optional
from fastapi import HTTPException

from sqlalchemy.orm import Session
import ast
import json
from ..schemas import graphs as graph_schema
from ..models import graph as graph_model


def create_graph(db: Session, new_graph: graph_schema.GraphSchema) -> graph_schema.GraphSchema:
    graph_create= graph_model.Graph(**new_graph.model_dump())
    new_graph=graph_model.Graph(name=graph_create.name, data=str(graph_create.data))
    db.add(new_graph)

    # Realizar la operación de confirmación para guardar los cambios en la base de datos
    db.commit()
    db.refresh(new_graph)
    # Devolver la instancia de Graph que acabas de añadir a la base de datos
    return new_graph



def fetch_graph_by_name(db: Session, graph_name: str) -> dict:
    graph = db.query(graph_model.Graph).filter(graph_model.Graph.name == graph_name).first()

    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")

    response = {"name": graph.name, "data": ast.literal_eval(graph.data)}
    print(response)
    return response
