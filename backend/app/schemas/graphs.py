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
    lineType: Optional[str] = Field(default="continue")


class GraphNode(BaseModel):
    id: str
    label: str
    data: Optional[Dict[str, Any]] = Field(default={})
    coordenates: Optional[NodeCoordenates]
    linkedTo: List[NodeEdge]

    def has_child(self, node_id: str, exclude_zero_weights=False) -> bool:
        return any(node.nodeId == node_id for node in self.linkedTo if node.weight != 0.0 or not exclude_zero_weights)

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

    def update_edge_weight(self, to_node_id: str, new_weight: float, color: str, lineType: str) -> bool:
        for edge in self.linkedTo:
            if edge.nodeId == to_node_id:
                edge.weight = new_weight
                edge.color = color
                edge.lineType = lineType
                return True

        raise Exception("Edge not found: " + self.id + " -> " + to_node_id, "Weight: " + str(new_weight))

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

    def get_in_out_neighbors_ids(self, nodeIds: List[str], exclude_zero_weights = False) -> List[str]:
        neighbors = set()

        for nodeId in nodeIds:
            for edge in self._nodesMap.get(nodeId).linkedTo:
                if edge.weight != 0.0 or not exclude_zero_weights:
                    neighbors.add(edge.nodeId)

            for node in self.get_nodes_pointing_to(nodeId, exclude_zero_weights=exclude_zero_weights):
                neighbors.add(node.id)

        return list(neighbors)

    def get_in_out_neighbors(self, nodeIds: List[str], exclude_zero_weights = False) -> List[GraphNode]:
        neighbors = self.get_in_out_neighbors_ids(nodeIds, exclude_zero_weights=exclude_zero_weights)
        nodes = []

        for n in neighbors:
            nodes.append(self._nodesMap.get(n))

        return nodes

    def get_children(self, nodeId: str, exclude_zero_weights = False) -> List[GraphNode]:
        if not exclude_zero_weights:
            return [self._nodesMap.get(edge.nodeId) for edge in self._nodesMap.get(nodeId).linkedTo]

        return [self._nodesMap.get(edge.nodeId) for edge in self._nodesMap.get(nodeId).linkedTo if edge.weight != 0.0]

    def update_edge_weight(self, from_node_id: str, to_node_id: str, new_weight: float, color: str = "#000", lineType: str = "continue") -> bool:
        from_node = self.get_node_by_id(from_node_id)
        if from_node:
            return from_node.update_edge_weight(to_node_id, new_weight, color, lineType)
        raise Exception("Node not found. "+from_node_id+" -> "+to_node_id+" Weight: "+str(new_weight))

    def remove_edge(self, from_node_id: str, to_node_id: str) -> bool:
        from_node = self.get_node_by_id(from_node_id)
        if from_node:
            return from_node.remove_edge_by_node_id(to_node_id)
        return False

    def get_nodes_pointing_to(self, node_id: str, exclude_zero_weights = False) -> List[GraphNode]:
        subscriptors = []

        for n in self.data:
            if n.has_child(node_id=node_id, exclude_zero_weights=exclude_zero_weights):
                subscriptors.append(n)

        return subscriptors