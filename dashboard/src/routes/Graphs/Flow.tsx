import React, { useRef } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
} from 'reactflow';
import { useParams } from 'react-router-dom';
import { useStoreWithEqualityFn } from 'zustand/traditional'

import VertexNode from './components/Vertex';
import { FlowContext, FlowState, createFlowStore } from '@/store/store';
import Toolbar from './components/Toolbar';

import 'reactflow/dist/style.css';
import './Flow.css';

const nodeTypes = { vertex: VertexNode }

const selector = (state: FlowState) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
  addNodes: state.addNodes,
});

export default function Flow({ inputNodes, inputEdges}: any) {
  const { graphId } = useParams()

  const store = useRef(
    createFlowStore({
      id: graphId,
      nodes: inputNodes || [],
      edges: inputEdges || [],
    })
  ).current

  const state = useStoreWithEqualityFn(store, selector)

  return (
    <FlowContext.Provider value={store}>
      <div style={{ width: '100%', height: '90vh', border: '#f2f2f2 2px solid'}}>
        <ReactFlow
          nodeTypes={nodeTypes}
          nodes={state.nodes}
          edges={state.edges}
          onNodesChange={state.onNodesChange}
          onEdgesChange={state.onEdgesChange}
          onConnect={state.onConnect}
          fitView
        >
          <Controls />
          <MiniMap />
          <Toolbar />
        </ReactFlow>
      </div>
    </FlowContext.Provider>
  );
}
