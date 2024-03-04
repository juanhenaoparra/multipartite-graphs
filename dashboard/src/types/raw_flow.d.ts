interface RawGraph {
  graph: Graph[];
}

interface Graph {
  name: string;
  data: Node[];
}

interface Node {
  id: string;
  label: string;
  coordenates: { x: number; y: number };
  radius: number;
  linkedTo: Edge[];
}

interface Edge {
  nodeId: number;
  weight: number;
}