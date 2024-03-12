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
  MarkerType,
} from 'reactflow';
import { ExportGraph } from '@/routes/Graphs/api/binding';
import { GenRandomHex } from '@/shared/id';

type NodeProps = {
  label?: string
}

interface FlowProps {
  id: string
  nodes: Node<NodeProps>[]
  edges: Edge[]
  nodesMap: Map<string, Node>
  edgesMap: Map<string, Edge>
}

interface FlowExportProps {
  blobURL: string
  filename: string
}

export interface FlowState extends FlowProps {
  onNodesChange: OnNodesChange
  onEdgesChange: OnEdgesChange
  onConnect: OnConnect
  setNodes: (nodes: Node[]) => void
  setEdges: (edges: Edge[]) => void
  getNodeById: (nodeId: string) => Node | undefined
  getEdgeById: (edgeId: string) => Edge | undefined
  addNodes: (nodes: Node[]) => void
  updateNodeData: (nodeId: string, data: NodeProps) => void
  updateNodeStyle: (nodeId: string, style: React.CSSProperties) => void
  updateEdgeData: (edgeId: string, data: any) => void
  updateEdgeStyle: (edgeId: string, style: React.CSSProperties) => void
  export: () => FlowExportProps
}

type FlowStore = ReturnType<typeof createFlowStore>

export const createFlowStore = (initProps?: Partial<FlowProps>) => {
  const defaultProps: FlowProps = {
    id: '',
    nodes: [],
    edges: [],
    nodesMap: new Map(),
    edgesMap: new Map(),
  }

  initProps.nodes?.forEach((node) => {
    initProps.nodesMap.set(node.id, node)
  })

  initProps.edges?.forEach((edge) => {
    initProps.edgesMap.set(edge.id, edge)
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
      const newEdge: Edge = {
        id: GenRandomHex(8),
        source: connection.source,
        target: connection.target,
        type: 'weightedge',
        markerEnd: { type: MarkerType.ArrowClosed },
        data: { weight: 0 },
      }

      set({
        edges: addEdge(newEdge, get().edges),
      });

      get().edgesMap.set(newEdge.id, newEdge);
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
      return get().nodes.find((node) => node.id === nodeId);
    },
    getEdgeById: (edgeId: string): Edge | undefined => {
      return get().edges.find((edge) => edge.id === edgeId);
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
            if (!node.style) {
              node.style = {}
            }

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
    updateEdgeData: (edgeId: string, data: any) => {
      set({
        edges: get().edges.map((edge) => {
          if (edge.id === edgeId) {
            if (!edge.data) {
              edge.data = {}
            }

            Object.keys(data).forEach((key) => {
              if (!!data[key]) {
                edge.data = {
                  ...edge.data,
                  [key]: data[key],
                };
              }
            })
          }

          return edge;
        })
      })
    },
    updateEdgeStyle: (edgeId: string, style: React.CSSProperties) => {
      set({
        edges: get().edges.map((edge) => {
          if (edge.id === edgeId) {
            Object.keys(style).forEach((key) => {
              if (!!style[key]) {
                edge.style = {
                  ...edge.style,
                  [key]: style[key],
                };
              }
            })
          }

          return edge;
        })
      })
    },
    export: (): FlowExportProps => {
      const graphId = get().id
      const rawGraph = ExportGraph(graphId, get().nodes, get().edges)
      let blob = new Blob([JSON.stringify(rawGraph)], {type: "application/json"})
      return {
        filename: graphId,
        blobURL: window.URL.createObjectURL(blob)
      }
    }
  }))
}

export const FlowContext = createContext<FlowStore | null>(null)

export function useFlowContext<T>(selector: (state: FlowState) => T): T {
  const store = useContext(FlowContext)
  if (!store) throw new Error('Missing FlowContext.Provider in the tree')

  return useStoreWithEqualityFn(store, selector)
}

