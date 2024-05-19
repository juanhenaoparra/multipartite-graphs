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

    def update_edge_weight(self, to_node_id: str, new_weight: float) -> bool:
        for edge in self.linkedTo:
            if edge.nodeId == to_node_id:
                edge.weight = new_weight
                return True
        return False

    def remove_edge_by_node_id(self, to_node_id: str) -> bool:
        for edge in self.linkedTo:
            if edge.nodeId == to_node_id:
                self.linkedTo.remove(edge)
                return True
        return False

class GraphSchema(BaseModel):
    name: str
    data: List[GraphNode]
    _nodesMap: Dict[str, GraphNode] = PrivateAttr(default_factory=dict)

    def set_nodes_map(self):
        self._nodesMap = {node.id: node for node in self.data}

    def get_node_by_id(self, nodeId: str) -> Optional[GraphNode]:
        return self._nodesMap.get(nodeId)

    def get_children(self, nodeId: str) -> List[GraphNode]:
        return [self._nodesMap.get(edge.nodeId) for edge in self._nodesMap.get(nodeId).linkedTo]

    def update_edge_weight(self, from_node_id: str, to_node_id: str, new_weight: float) -> bool:
        from_node = self.get_node_by_id(from_node_id)
        if from_node:
            return from_node.update_edge_weight(to_node_id, new_weight)
        return False

    def remove_edge(self, from_node_id: str, to_node_id: str) -> bool:
        from_node = self.get_node_by_id(from_node_id)
        if from_node:
            return from_node.remove_edge_by_node_id(to_node_id)
        return False