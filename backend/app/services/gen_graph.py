from typing import Dict, List
import random

from app.schemas.generation import GenGraphInput, AdjacencyNode
from app.schemas.graphs import GraphSchema, GraphNode, NodeEdge
from app.services.ids import GenRandomHex

DEFAULT_WEIGHT_START = 0.0
DEFAULT_WEIGHT_END = 1.0
INFINITE_WEIGHT = float('inf')
MATCHING_WEIGHT = -1

def generateNodeLabels(numNodes: int) -> List[str]:
    """
    Generate a list of node labels from 'A' onwards for the given number of nodes.
    """
    labels = []
    for i in range(numNodes):
        labels.append(chr(65 + i))  # 65 is the ASCII value for 'A'
    return labels

def generateBipartiteGraph(presentNodesCount: int, futureNodesCount: int) -> Dict[str, List[AdjacencyNode]]:
    """
    Generate a bipartite graph with the given number of present and future nodes.
    All edges have infinite weight except when connecting corresponding present to future nodes,
    which have a weight of -1.
    If the number of present nodes equals the number of future nodes, no edge is created
    between corresponding present and future nodes.
    """
    presentNodes = generateNodeLabels(presentNodesCount)
    futureNodes = [label + "'" for label in generateNodeLabels(futureNodesCount)]

    adjacencyList: Dict[str, List[AdjacencyNode]] = {}

    for pNode in presentNodes:
        if pNode not in adjacencyList:
            adjacencyList[pNode] = []

        for fNode in futureNodes:
            if pNode + "'" == fNode:
                continue  # Skip creating an edge between corresponding nodes
            weight = MATCHING_WEIGHT if pNode + "'" == fNode else INFINITE_WEIGHT
            adjacencyList[pNode].append(AdjacencyNode(
                id=fNode,
                parentId=pNode,
                weight=weight
            ))

            adjacencyList[fNode] = []

    return adjacencyList

def generateGraphComplete(nodesNumber: int, isWeighted: bool = False) -> Dict[str, List[AdjacencyNode]]:
    """
    Generate a complete graph with a given number of nodes.
    """
    adjacencyList: Dict[str, List[AdjacencyNode]] = {}

    for i in range(nodesNumber):
        nodeIndex = getNodeId(i)

        if nodeIndex not in adjacencyList:
            adjacencyList[nodeIndex] = []

        for j in range(nodesNumber):
            if i == j:
                continue

            adjacencyList[nodeIndex].append(AdjacencyNode(
                id=str(j),
                parentId=nodeIndex,
                weight=GetRandomWithPrecision(DEFAULT_WEIGHT_START, DEFAULT_WEIGHT_END) if isWeighted else None))

    return adjacencyList



def generateGraphConnected(nodesNumber: int, degree: int, rewireProbability: float, isWeighted: bool = False) -> Dict[str, List[AdjacencyNode]]:
    """"
    Generate a connected graph with a given number of nodes and a given degree by using
    the Watts-Strogatz model. https://en.wikipedia.org/wiki/Watts%E2%80%93Strogatz_model#Algorithm
    """
    adjacencyList: Dict[str, List[AdjacencyNode]] = {}

    for i in range(nodesNumber):
        index = getNodeId(i)

        if i not in adjacencyList:
            adjacencyList[index] = []

        firstKNeighbors = findNearestNeighbor(i, degree+1, nodesNumber-1)

        for j in firstKNeighbors:
            if i == j:
                continue

            adjacencyList[index].append(AdjacencyNode(
                id=str(j),
                parentId=index,
                weight=GetRandomWithPrecision(DEFAULT_WEIGHT_START, DEFAULT_WEIGHT_END) if isWeighted else None))

    adjacencyListKeys = list(adjacencyList.keys())

    for nodeIndex, nodeName in enumerate(adjacencyListKeys):
        for k in range(degree//2):
            if random.random() > rewireProbability:
                continue

            kthNodeIndex = random.choice([i for i in range(nodesNumber) if i != nodeIndex])
            kthNode = adjacencyListKeys[kthNodeIndex]

            if kthNode is None:
                continue

            adjacencyList[nodeName][k].id = kthNode

    return adjacencyList

def generateGraphRandom(nodesNumber: int, degree: int, isWeighted: bool = False) -> Dict[str, List[AdjacencyNode]]:
    """"
    Generate a connected graph with a given number of nodes and a given degree by using
    the Erdos-Renyi model. https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93R%C3%A9nyi_model#Definition
    """
    adjacencyList: Dict[str, List[AdjacencyNode]] = {}

    for i in range(nodesNumber):
        index = getNodeId(i)

        if i not in adjacencyList:
            adjacencyList[index] = []

        kthNodeIndex = random.choice([j for j in range(nodesNumber) if j != i])

        adjacencyList[index].append(AdjacencyNode(
            id=str(kthNodeIndex),
            parentId=index,
            weight=GetRandomWithPrecision(DEFAULT_WEIGHT_START, DEFAULT_WEIGHT_END) if isWeighted else None))

    return adjacencyList

def getNodeId(index: int):
    return str(index)

def findNearestNeighbor(currentIndex: int, neighborSize: int, lastIndex: int) -> range:
    if currentIndex > lastIndex:
        raise ValueError(f"Current index {currentIndex} is greater than the last index {lastIndex}")

    neighborSize = neighborSize if lastIndex >= neighborSize else lastIndex
    halfNeighborSize = neighborSize // 2
    halfNeighborSizeRemainder = neighborSize % 2
    startSequence = currentIndex - halfNeighborSize
    endSequence = currentIndex + (halfNeighborSize+halfNeighborSizeRemainder)

    if startSequence < 0:
        return range(0, neighborSize)

    if endSequence > lastIndex:
        return range((lastIndex+1) - neighborSize, lastIndex+1)

    return range(startSequence, endSequence)

def GenerateGraph(genInput: GenGraphInput):
    """
    Generate a graph of N nodes based on the given input.
    Could be complete, connected or random.
    Also it could be weighted or not.
    """
    if genInput.complete:
        return generateGraphComplete(
            nodesNumber=genInput.nodesNumber,
            isWeighted=genInput.weighted)

    if genInput.connected:
        return generateGraphConnected(
            nodesNumber=genInput.nodesNumber,
            rewireProbability=genInput.probability,
            degree=genInput.degree,
            isWeighted=genInput.weighted,)
    if genInput.isBipartite:
        return  generateBipartiteGraph(
            presentNodesCount =genInput.presentNodesCount,
            futureNodesCount = genInput.futureNodesCount
        )

    return generateGraphRandom(
        nodesNumber=genInput.nodesNumber,
        degree=genInput.degree,
        isWeighted=genInput.weighted
    )

def GetRandomWithPrecision(start: float, end: float, precision: int = 2) -> float:
    return round(random.uniform(start, end), precision)

def TransformToGraphSchema(adjacencyList: Dict[str, List[AdjacencyNode]]) -> GraphSchema:
    """
    Transform an adjacency list to a GraphSchema object.
    """
    g = GraphSchema(name=GenRandomHex(16), data=[])

    for nodeId, neighborhood in adjacencyList.items():
        node = GraphNode(
            id=nodeId,
            label=nodeId,
            coordenates={"x": GetRandomWithPrecision(0, 1000), "y": GetRandomWithPrecision(0, 1000)},
            linkedTo=[]
        )

        g.data.append(node)

        for neighbor in neighborhood:
            node.linkedTo.append(NodeEdge(
                nodeId=neighbor.id,
                weight=neighbor.weight if neighbor.weight else None
            ))

    return g