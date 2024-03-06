import React, { memo, useCallback } from "react";
import { useReactFlow, Handle, Position, NodeToolbar } from "reactflow";
import { useFlowContext } from "@/store/store";
import VertexPropertyRename from "./VertexPropertyRename";
import VertexPropertyColor from "./VertexPropertyColor";

export default memo(({ id, data, isConnectable }: any) => {
  const { setNodes, setEdges } = useReactFlow();
  const getNodeById = useFlowContext((s) => s.getNodeById);

  const node = getNodeById(id);

  const deleteNode = useCallback(() => {
    setNodes((nodes) => nodes.filter((node) => node.id !== id));
    setEdges((edges) => edges.filter((edge) => edge.source !== id));
  }, [id, setNodes, setEdges]);

  return (
    <>
      <NodeToolbar
        isVisible={data.toolbarVisible}
        position={Position.Right}
        offset={20}
        className="node-toolbar"
      >
        <h4 onClick={() => navigator.clipboard.writeText(id)}>{id}</h4>
        <VertexPropertyRename id={id} node={node} visible={!!node}/>
        <button onClick={deleteNode}>delete</button>
        <VertexPropertyColor id={id} node={node} visible={!!node}/>
      </NodeToolbar>

      <div className="vertex-label">{data.label}</div>

      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </>
  );
});
