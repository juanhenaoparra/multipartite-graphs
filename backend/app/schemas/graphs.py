from typing import List
from pydantic import BaseModel

class NodeCoordenates(BaseModel):
    x: float
    y: float

class NodeEdge(BaseModel):
    nodeId: str
    weight: float

class GraphNode(BaseModel):
    id: str
    label: str
    coordenates: NodeCoordenates
    linkedTo: List[NodeEdge] 
    
class GraphSchema(BaseModel):
    name: str
    data: List[GraphNode]



