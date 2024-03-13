interface RawGraph {
  graph: Graph[];
}

interface Graph {
  name: string;
  data: GraphNode[];
}

interface GraphNodeData {
  color?: string;
  backgroundColor?: string;
}

interface GraphNode {
  id: string;
  label: string;
  radius: number;
  data?: GraphNodeData;
  coordenates: { x: number; y: number };
  linkedTo: GraphEdge[];
}

interface GraphEdge {
  nodeId: string;
  weight: number;
  color?: string;
  lineType?: string;
}