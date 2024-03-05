import { GenRandomHex } from '@/shared/id';
import {
  Node,
  Edge,
} from 'reactflow';

const radiusFactor = 90;

export function GetNodeStyle(data: any) {
  return {
    width: data.radius*radiusFactor,
    height: data.radius*radiusFactor,
    backgroundColor: data.color || '#efefef',
  }
}

export function ParseGraph(graph: RawGraph) {
  const nodes: Array<Node> = graph.graph[0].data.map((node) => ({
    id: node.id.toString(),
    type: 'vertex',
    position: { x: node.coordenates.x, y: node.coordenates.y },
    data: { label: node.label },
    style: GetNodeStyle(node),
    className: 'vertex-circle'
  }));

  const edges: Array<Edge> = graph.graph[0].data
    .map((node) => node.linkedTo.map((edge) => ({
      id: `e${node.id}-${edge.nodeId}`,
      source: node.id.toString(),
      target: edge.nodeId.toString() })))
    .flat();

  return {
    initialNodes: nodes,
    initialEdges: edges
  };
}

export function GenGraph(size: number) {
  let initialNodes: Array<Node> = [];
  let initialEdges: Array<Edge> = [];

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