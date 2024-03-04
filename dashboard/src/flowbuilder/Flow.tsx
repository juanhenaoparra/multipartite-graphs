import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';

import graph from './graphs.json';
import { GetFlow } from './storage';
import VertexNode from './Vertex';

const radiusFactor = 90;

function getNodeStyle(data: any) {
  return {
    width: data.radius*radiusFactor,
    height: data.radius*radiusFactor,
    backgroundColor: data.color || '#efefef',
  }
}

function parseGraph(graph: RawGraph) {
  const nodes: Array<Node> = graph.graph[0].data.map((node) => ({
    id: node.id.toString(),
    type: 'vertex',
    position: { x: node.coordenates.x, y: node.coordenates.y },
    data: { label: node.label },
    style: getNodeStyle(node),
    className: 'vertex-circle'
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
  let initialNodes: Array<Node> = [];
  let initialEdges: Array<Edge> = [];

  for (let i = 0; i < size; i++) {
    initialNodes.push({
      id: i.toString(),
      position: { x: Math.random() * 1000, y: Math.random() * 1000 },
      data: { label: `Node ${i}` },
      style: { width: 80 },
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

const getNodeId = () => `randomnode_${+new Date()}`;

const nodeTypes = {vertex: VertexNode}

export default function Flow() {
  // const { flow } = useLoaderData();

  const { initialNodes, initialEdges } = parseGraph(graph as unknown as RawGraph);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const onAdd = useCallback(() => {
    const newNode = {
      id: getNodeId(),
      type: 'vertex',
      data: { label: 'New Node' },
      position: {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      },
      style: getNodeStyle({radius: 1, color: '#efefef'  }),
      className: 'vertex-circle'
    }

    setNodes((nodes) => nodes.concat(newNode))
  }, [setNodes])

  return (
    <>
      <div style={{ width: '85vw', height: '90vh' }}>
        <ReactFlow
          nodeTypes={nodeTypes}
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
        >
          <Controls />
          <MiniMap />
          <Panel position="top-left">
            <button onClick={onAdd} className="main-panel__button">
              <img src="/new_icon.svg"/>
              add vertex
            </button>
          </Panel>
        </ReactFlow>
      </div>
    </>
  );
}
