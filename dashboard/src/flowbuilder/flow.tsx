import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { RawGraph } from '@/types/raw_flow';

import graph from './graphs.json';

function parseGraph(graph: RawGraph) {
  const nodes = graph.graph[0].data.map((node) => ({
    id: node.id.toString(),
    position: { x: node.coordenates.x, y: node.coordenates.y },
    data: { label: node.label },
  }));

  const edges = graph.graph[0].data
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

function genGraph(size: number) {
  let initialNodes = [];
  let initialEdges = [];

  for (let i = 0; i < size; i++) {
    initialNodes.push({
      id: i.toString(),
      position: { x: Math.random() * 1000, y: Math.random() * 1000 },
      data: { label: `Node ${i}` },
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

export default function Flow() {
  const { initialNodes, initialEdges } = genGraph(50);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
