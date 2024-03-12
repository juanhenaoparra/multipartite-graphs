import React, { useEffect, useRef } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
} from 'reactflow';
import { useParams } from 'react-router-dom';
import { useStoreWithEqualityFn } from 'zustand/traditional'

import { FlowContext, FlowState, createFlowStore } from '@/store/store';
import ToolsPanel from './components/ToolsPanel';
import WeightEdge from './components/WeightEdge';
import VertexNode from './components/Vertex';

import 'reactflow/dist/style.css';
import './Flow.css';
import { GetFlow } from './api/api';
import { ParseGraph } from './api/binding';
import axios from 'axios';

const nodeTypes = { vertex: VertexNode }
const edgeTypes = {
  weightedge: WeightEdge,
};

const selector = (state: FlowState) => ({
  nodes: state.nodes,
  edges: state.edges,
  onNodesChange: state.onNodesChange,
  onEdgesChange: state.onEdgesChange,
  onConnect: state.onConnect,
});

export default function Flow({ inputNodes, inputEdges}: any) {
  const { graphId } = useParams()

  useEffect(() => {
    if (
      graphId == '' ||
      (inputNodes && inputNodes.length > 0) ||
      (inputEdges && inputEdges.length > 0)
    ) {
      return
    }

    GetFlow(graphId).then((flow) => {
      const {initialNodes, initialEdges} = ParseGraph(flow)

      inputNodes = initialNodes
      inputEdges = initialEdges
    }).catch((err) => {
      if (!axios.isAxiosError(err)) {
        throw err
      }

      if (!err.response) {
        throw err
      }

      if (err.response.status == 404) {
        console.warn(`Graph not found: ${graphId}`)
        return
      }

      throw err
    })
  }, [graphId])

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
          edgeTypes={edgeTypes}
          nodes={state.nodes}
          edges={state.edges}
          onNodesChange={state.onNodesChange}
          onEdgesChange={state.onEdgesChange}
          onConnect={state.onConnect}
          fitView
        >
          <Controls />
          <MiniMap />
          <ToolsPanel />
        </ReactFlow>
      </div>
    </FlowContext.Provider>
  );
}
