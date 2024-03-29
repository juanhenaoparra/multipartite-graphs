from typing import Optional
from fastapi import HTTPException

from sqlalchemy.orm import Session
import ast
from ..schemas import graphs as graph_schema
from ..schemas import generation as gen_schema
from ..models import graph as graph_model
from ..services.gen_graph import GenerateGraph, TransformToGraphSchema

def create_graph(db: Session, new_graph: graph_schema.GraphSchema) -> graph_schema.GraphSchema:
    existing_graph = db.query(graph_model.Graph).filter_by(name=new_graph.name).first()
    graph_create = graph_model.Graph(**new_graph.model_dump())

    if existing_graph:
        # Si existe un grafo con el mismo nombre, actualizarlo
        existing_graph.data = str(graph_create.data)
        db.commit()
        db.refresh(existing_graph)
        return existing_graph
    else:
        # Si no existe un grafo con el mismo nombre, crear uno nuevo
        new_graph = graph_model.Graph(name=graph_create.name, data=str(graph_create.data))
        db.add(new_graph)
        db.commit()
        db.refresh(new_graph)
        return new_graph

def fetch_graph_by_name(db: Session, graph_name: str) -> dict:
    graph = db.query(graph_model.Graph).filter(graph_model.Graph.name == graph_name).first()

    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")

    response = {"name": graph.name, "data": ast.literal_eval(graph.data)}
    return response

def create_random_graph(db: Session, graph_input: gen_schema.GenGraphInput):
    if graph_input.nodesNumber <= 0:
        raise HTTPException(status_code=400, detail="The number of nodes must be greater than 0")

    adjacencyList = GenerateGraph(graph_input)
    graph = TransformToGraphSchema(adjacencyList=adjacencyList)

    newGraphAsDict = graph.model_dump()
    newGraphModel = graph_model.Graph(name=graph.name, data=str(newGraphAsDict["data"]))
    db.add(newGraphModel)
    db.commit()
    db.refresh(newGraphModel)

    return graph
