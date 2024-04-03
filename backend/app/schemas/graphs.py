from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, PrivateAttr, field_validator

class NodeProperties(str, Enum):
    VISITED = "visited"
    BACKGROUND_COLOR = "backgroundColor"


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

    def has_child(self, node_id: str) -> bool:
        return any(node.nodeId == node_id for node in self.linkedTo)

    def set_property(self, key: Union[str, NodeProperties], value: Any) -> None:
        if isinstance(key, NodeProperties):
            key = key.value

        self.data[key] = value

    def pop_property(self, key: Union[str, NodeProperties]) -> Optional[Any]:
        if isinstance(key, NodeProperties):
            key = key.value

        if key not in self.data:
            return None

        return self.data.pop(key)

    def has_property(self, key: Union[str, NodeProperties], value = None) -> bool:
        if isinstance(key, NodeProperties):
            key = key.value

        key_exists = key in self.data and self.data[key] is not None and len(self.data[key]) > 0

        if value is None:
            return key_exists

        return key_exists and self.data[key] == value


class GraphSchema(BaseModel):
    name: str
    data: List[GraphNode]
    _nodesMap: Dict[str, GraphNode] = PrivateAttr(dict)

    def set_nodes_map(self):
        self._nodesMap = {node.id: node for node in self.data}

    def get_node_by_id(self, nodeId: str) -> GraphNode:
        return self._nodesMap.get(nodeId)

    def get_children(self, nodeId: str) -> List[GraphNode]:
        return [self._nodesMap.get(edge.nodeId) for edge in self._nodesMap.get(nodeId).linkedTo]

