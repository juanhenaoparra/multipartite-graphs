export interface RawGraph {
  graph: Graph[];
}

export interface Graph {
  name: string;
  data: Node[];
}

export interface Node {
  id: number;
  label: string;
  coordenates: { x: number; y: number };
  radius: number;
  linkedTo: Edge[];
}

export interface Edge {
  nodeId: number;
  weight: number;
}