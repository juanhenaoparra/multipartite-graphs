interface RawGraph {
  graph: Graph[];
}

interface Graph {
  name: string;
  data: GraphNode[];
}

interface GraphNode {
  id: string;
  label: string;
  coordenates: { x: number; y: number };
  radius: number;
  linkedTo: GraphEdge[];
}

interface GraphEdge {
  nodeId: string;
  weight: number;
}