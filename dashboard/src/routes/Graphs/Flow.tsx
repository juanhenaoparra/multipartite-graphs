import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  useNodesState,
  useEdgesState,
  addEdge,
  Panel,
} from 'reactflow';
import { useParams } from 'react-router-dom';

import VertexNode from './components/Vertex';
import { GetNodeStyle } from './storage/binding';
import { GenRandomHex } from '@/shared/id';

import NewIcon  from '@/assets/new_icon.svg?react';
import 'reactflow/dist/style.css';
import './Flow.css';

const getNodeId = () => `randomnode_${GenRandomHex(8)}`;
const nodeTypes = { vertex: VertexNode }

export default function Flow({ inputNodes, inputEdges}: any) {
  const { graphId } = useParams();

  const [nodes, setNodes, onNodesChange] = useNodesState(inputNodes || []);
  const [edges, setEdges, onEdgesChange] = useEdgesState(inputEdges || []);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const onAdd = useCallback(() => {
    const newNode = {
      id: getNodeId(),
      type: 'vertex',
      data: { label: 'My new node' },
      position: {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      },
      style: GetNodeStyle({radius: 1, color: '#efefef'  }),
      className: 'vertex-circle'
    }

    setNodes((nodes) => nodes.concat(newNode))
  }, [setNodes])

  return (
    <>
      <div style={{ width: '100%', height: '90vh', border: '#f2f2f2 2px solid'}}>
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
              <NewIcon/>
              add
            </button>
          </Panel>
        </ReactFlow>
      </div>
    </>
  );
}
