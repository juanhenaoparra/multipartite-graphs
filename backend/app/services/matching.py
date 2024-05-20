from typing import List
from app.schemas.graphs import GraphSchema, NodeProperties
from app.schemas.bipartite import BipartiteMatchResponse

class NotBipartiteException(Exception):
    pass

class CheckBipartite:
    def __init__(self, g: GraphSchema, availableColors: List[str] = ["#cfe2f3", "#ffd28b"]) -> None:
        self.g = g
        self.colors = availableColors
        self.exclude_zero_weights = False
        self.colored = {}
        self.g.set_nodes_map()

        for node in self.g.data:
            node.pop_property(NodeProperties.BACKGROUND_COLOR)

    def set_color(self, nodeId, color):
        self.colored[nodeId] = color

        self.g.get_node_by_id(nodeId).set_property(NodeProperties.BACKGROUND_COLOR, self.colors[color])

    def process(self) -> BipartiteMatchResponse:
        """
        Receives a graph and determines if it is bipartite.
        The algorithm is based on the fact that a graph is bipartite if and only if it is 2-colorable.
        """
        res = BipartiteMatchResponse(isBipartite=False)

        for node in self.g.data:
            nodeGroup = res.get_node_group(node.id)
            if nodeGroup == -1:
                nodeGroup = res.get_max_group() + 1

            if node.id in self.colored: # skip already colored nodes
                continue

            children = self.g.get_children(node.id, exclude_zero_weights=self.exclude_zero_weights)
            if (children is None or len(children) == 0) and (self.g.get_nodes_pointing_to(node.id) == 0): # set first color to isolated nodes
                self.set_color(node.id, 0)
                res.add_node_to_group(node.id, nodeGroup)
                continue

            queue = [node]
            self.set_color(node.id, 1)
            childrenToAdd = {node.id}

            while queue:
                v = queue.pop()
                oppositeColor = 1 - self.colored[v.id]

                for child in self.g.get_children(v.id, exclude_zero_weights=self.exclude_zero_weights):
                    childrenToAdd.add(child.id)
                    auxGroup = res.get_node_group(child.id)
                    if auxGroup != -1: # change group if any child already belongs to a group
                        nodeGroup = auxGroup

                    if child.id in self.colored:
                        if self.colored[child.id] == self.colored[v.id]:
                            raise NotBipartiteException("graph is not bipartite")
                    else:
                        self.set_color(child.id, oppositeColor)
                        queue.append(child)

            for c in childrenToAdd:
                res.add_node_to_group(c, nodeGroup)

        res.isBipartite = True

        return res


def pick_opposite_color(color: str, colorsList: List[str]) -> str:
    opporsites = [c for c in colorsList if c != color]

    return opporsites[0]