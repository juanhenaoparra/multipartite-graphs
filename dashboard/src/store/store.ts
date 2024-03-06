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
  label?: string
}

interface FlowProps {
  id: string
  nodes: Node<NodeProps>[]
  edges: Edge[]
  nodesMap: Map<string, Node>
}

export interface FlowState extends FlowProps {
  onNodesChange: OnNodesChange
  onEdgesChange: OnEdgesChange
  onConnect: OnConnect
  setNodes: (nodes: Node[]) => void
  setEdges: (edges: Edge[]) => void
  getNodeById: (nodeId: string) => Node | undefined
  addNodes: (nodes: Node[]) => void
  updateNodeData: (nodeId: string, data: NodeProps) => void
  updateNodeStyle: (nodeId: string, style: React.CSSProperties) => void
}

type FlowStore = ReturnType<typeof createFlowStore>

export const createFlowStore = (initProps?: Partial<FlowProps>) => {
  const defaultProps: FlowProps = {
    id: '',
    nodes: [],
    edges: [],
    nodesMap: new Map(),
  }

  initProps.nodes?.forEach((node) => {
    initProps.nodesMap.set(node.id, node)
  })

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
    getNodeById: (nodeId: string): Node | undefined => {
      return get().nodesMap.get(nodeId);
    },
    addNodes: (nodes: Node[]) => {
      nodes.forEach((node) => {
        get().nodesMap.set(node.id, node);
      });

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
    },
    updateNodeStyle: (nodeId: string, style: React.CSSProperties) => {
      set({
        nodes: get().nodes.map((node) => {
          if (node.id === nodeId) {
            Object.keys(style).forEach((key) => {
              if (!!style[key]) {
                node.style = {
                  ...node.style,
                  [key]: style[key],
                };
              }
            })
          }

          return node;
        })
      })
    },
  }))
}

export const FlowContext = createContext<FlowStore | null>(null)

export function useFlowContext<T>(selector: (state: FlowState) => T): T {
  const store = useContext(FlowContext)
  if (!store) throw new Error('Missing FlowContext.Provider in the tree')

  return useStoreWithEqualityFn(store, selector)
}

