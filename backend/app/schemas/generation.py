from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional

class EdgesDirection(Enum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"

class GenGraphInput(BaseModel):
    nodesNumber: int = Field(description="Number of nodes in the graph")
    direction: EdgesDirection = Field(default=EdgesDirection.UNDIRECTED, description="Direction of the edges")
    weighted: bool = Field(default=False, description="If the graph is weighted or not")
    connected: bool = Field(default=False, description="If the graph is connected or not")
    isBipartite: bool = Field(default= False, description ="If the graph is Bipartite or not" )
    complete: bool = Field(default=False, description="If the graph is complete or not")
    probability: float = Field(default=0.5, description="Probability of a node being connected to another node, between 0.0 and 1.0, by default 0.5", ge=0.0, le=1.0)
    degree: int = Field(default=2, description="Expected degree of the graph, by default 2", gt=0)
    presentNodesCount: int= Field(default = 0)
    futureNodesCount:int = Field(default = 0)
class AdjacencyNode(BaseModel):
    id: str
    parentId: str
    weight: Optional[float]