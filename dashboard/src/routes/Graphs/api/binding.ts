import { GenRandomHex } from '@/shared/id';
import {
  Node as RFNode,
  Edge as RFEdge,
} from 'reactflow';

export const RADIUS_FACTOR = 90;

export function GetNodeStyle(data: any) {
  return {
    width: data.radius*RADIUS_FACTOR,
    height: data.radius*RADIUS_FACTOR,
    backgroundColor: data.color || '#efefef',
  }
}

export function ParseGraph(graph: RawGraph) {
  const nodes: Array<RFNode> = graph.graph[0].data.map((node) => ({
    id: node.id.toString(),
    type: 'vertex',
    position: { x: node.coordenates.x, y: node.coordenates.y },
    data: { label: node.label, radius: node.radius },
    style: GetNodeStyle(node),
    className: 'vertex-circle'
  }));

  const edges: Array<RFEdge> = graph.graph[0].data
    .map((node) => node.linkedTo.map((edge) => ({
      type: "default",
      id: `e${node.id}-${edge.nodeId}`,
      source: node.id.toString(),
      target: edge.nodeId.toString(),
      data: {
        weight: edge.weight,
      },
    })))
    .flat();

  return {
    initialNodes: nodes,
    initialEdges: edges
  };
}

export function ExportGraph(id: string, nodes: RFNode[], edges: RFEdge[]): RawGraph {
  let graph: Graph = {
    name: id,
    data: []
  }

  const exportGraph: RawGraph = {
    graph: [
      graph
    ]
  }

  graph.data = nodes.map(node => {
    const graphNode: GraphNode = {
      id: node.id,
      label: node.data?.label || "empty_label",
      radius: node.data?.radius,
      coordenates: {
        x: node.position.x,
        y: node.position.y,
      },
      linkedTo: []
    }

    const foundEdges = edges.filter((edge => {
      return edge.source == node.id
    }))

    foundEdges.forEach(edge => {
      graphNode.linkedTo.push({
        nodeId: node.id,
        weight: edge.data?.weight
      })
    })

    return graphNode
  })

  return exportGraph
}

export function GenGraph(size: number) {
  let initialNodes: Array<RFNode> = [];
  let initialEdges: Array<RFEdge> = [];

  for (let i = 0; i < size; i++) {
    initialNodes.push({
      id: GenRandomHex(8),
      type: 'vertex',
      position: { x: Math.random() * 1000, y: Math.random() * 1000 },
      data: { label: `Node ${i}` },
      style: GetNodeStyle({radius: 1, color: '#efefef'  }),
    });
  }

  for (let i = 0; i < size; i++) {
    const source = Math.floor(Math.random() * size);
    const target = Math.floor(Math.random() * size);

    initialEdges.push({
      id: `e${i}-${source}-${target}`,
      source: source.toString(),
      target: target.toString(),
    });
  }

  return {initialNodes, initialEdges}
}