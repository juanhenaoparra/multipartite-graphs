import { createContext, useContext } from 'react'
import { createStore } from 'zustand';
import { useStoreWithEqualityFn } from 'zustand/traditional'
import {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';

type NodeProps = {
  color?: string
  label?: string
}

interface FlowProps {
  id: string
  nodes: Node<NodeProps>[]
  edges: Edge[]
}

export interface FlowState extends FlowProps {
  onNodesChange: OnNodesChange
  onEdgesChange: OnEdgesChange
  onConnect: OnConnect
  setNodes: (nodes: Node[]) => void
  setEdges: (edges: Edge[]) => void
  addNodes: (nodes: Node[]) => void
  updateNodeData: (nodeId: string, data: NodeProps) => void
}

type FlowStore = ReturnType<typeof createFlowStore>

export const createFlowStore = (initProps?: Partial<FlowProps>) => {
  const defaultProps: FlowProps = {
    id: '',
    nodes: [],
    edges: [],
  }

  return createStore<FlowState>()((set, get) => ({
    ...defaultProps,
    ...initProps,
    onNodesChange: (changes: NodeChange[]) => {
      set({
        nodes: applyNodeChanges(changes, get().nodes),
      });
    },
    onEdgesChange: (changes: EdgeChange[]) => {
      set({
        edges: applyEdgeChanges(changes, get().edges),
      });
    },
    onConnect: (connection: Connection) => {
      set({
        edges: addEdge(connection, get().edges),
      });
    },
    setNodes: (nodes: Node[]) => {
      if (nodes.length === 0) {
        return;
      }

      set({ nodes });
    },
    setEdges: (edges: Edge[]) => {
      if (edges.length === 0) {
        return;
      }

      set({ edges });
    },
    addNodes: (nodes: Node[]) => {
      set({
        nodes: [...get().nodes, ...nodes]
      });
    },
    updateNodeData: (nodeId: string, data: NodeProps) => {
      set({
        nodes: get().nodes.map((node) => {
          if (node.id === nodeId) {
            Object.keys(data).forEach((key) => {
              if (!!data[key]) {
                node.data = {
                  ...node.data,
                  [key]: data[key],
                };
              }
            })
          }

          return node;
        })
      })
    }
  }))
}

export const FlowContext = createContext<FlowStore | null>(null)

export function useFlowContext<T>(selector: (state: FlowState) => T): T {
  const store = useContext(FlowContext)
  if (!store) throw new Error('Missing FlowContext.Provider in the tree')

  return useStoreWithEqualityFn(store, selector)
}

