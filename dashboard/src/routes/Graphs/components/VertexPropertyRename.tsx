import { useFlowContext } from "@/store/store"
import React, { useCallback, useState } from "react"
import { Node } from "reactflow"

const MAX_LABEL_LENGTH = 30

interface VertexPropertyRenameProps {
  id: string
  node: Node
  visible: boolean
}

export default function VertexPropertyRename({id, node, visible}: VertexPropertyRenameProps) {
  if (!visible || !node) return null

  const [showRenameInput, setShowRenameInput] = useState(false)
  const [nodeLabel, setNodeLabel] = useState(node.data.label)

  const updateNodeData = useFlowContext((s) => s.updateNodeData);

  const changeNodeLabel = useCallback(
    (newLabel: string) => {
      if (newLabel === node.data.label) return
      if (newLabel.length > MAX_LABEL_LENGTH) return

      updateNodeData(id, {label: newLabel});
    },
    [id]
  );

  return (
    <>
      {
        !showRenameInput &&
        <button onClick={() => {setShowRenameInput(true)}}>
          rename
        </button>
      }
      {
        !!showRenameInput &&
        <input
          type="text"
          value={nodeLabel}
          onChange={(e) => {
            setNodeLabel(e.target.value)
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              changeNodeLabel(nodeLabel)
              setShowRenameInput(false)
            }
          }}
          maxLength={MAX_LABEL_LENGTH}
        />
      }
    </>
  )
}