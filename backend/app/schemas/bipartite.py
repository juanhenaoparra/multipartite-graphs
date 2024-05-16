from typing import List, Dict
from app.schemas.graphs import GraphNode
from pydantic import BaseModel

class BipartiteMatchResponse(BaseModel):
    isBipartite: bool
    reason: str = None
    connectedComponents: Dict[int, List[str]] = {}

    def add_node_to_group(self, nodeId: str, groupNumber: int):
        if self.connectedComponents.get(groupNumber) is None:
            self.connectedComponents[groupNumber] = []

        if nodeId in self.connectedComponents[groupNumber]:
            return

        self.connectedComponents[groupNumber].append(nodeId)

    def get_node_group(self, nodeId: str):
        for group, nodes in self.connectedComponents.items():
            if nodeId in nodes:
                return group

        return -1

    def get_max_group(self) -> int:
        if len(self.connectedComponents) == 0:
            return 0

        return max(self.connectedComponents.keys())

class SystemPartitionInput(BaseModel):
    full_system: List[List[float]]
    matrix: List[List[int]]
    binary_distribution: str
