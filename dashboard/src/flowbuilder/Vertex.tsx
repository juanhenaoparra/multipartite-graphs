import React, { memo, useCallback } from 'react';
import { useReactFlow, Handle, Position, NodeToolbar } from 'reactflow';

export default memo(({ id, data, isConnectable }) => {
  const { getNode, setNodes, setEdges } = useReactFlow();

  const deleteNode = useCallback(() => {
    const node = getNode(id);

    setNodes((nodes) => nodes.filter((node) => node.id !== id));
    setEdges((edges) => edges.filter((edge) => edge.source !== id));
  }, [id, setNodes, setEdges]);


  return (
    <>
      <NodeToolbar isVisible={data.toolbarVisible} position={data.toolbarPosition}>
        <button onClick={deleteNode}>delete</button>
        <button>copy</button>
      </NodeToolbar>

      <div className="vertex-label">
        {data.label}
      </div>

      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </>
  )
})
