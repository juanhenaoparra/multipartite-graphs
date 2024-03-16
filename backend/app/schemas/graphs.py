from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class NodeCoordenates(BaseModel):
    x: float
    y: float

class NodeEdge(BaseModel):
    nodeId: str
    weight: Optional[float]
    color: Optional[str] = Field(default="#000000")

class GraphNode(BaseModel):
    id: str
    label: str
    data: Optional[Dict[str, Any]] = Field(default={})
    coordenates: Optional[NodeCoordenates]
    linkedTo: List[NodeEdge]

class GraphSchema(BaseModel):
    name: str
    data: List[GraphNode]



