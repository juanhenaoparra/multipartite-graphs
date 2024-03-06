import { useFlowContext } from "@/store/store"
import React, { useCallback, useState } from "react"
import { Node } from "reactflow"

interface VertexPropertyColorProps {
  id: string
  node: Node
  visible: boolean
}

export default function VertexPropertyColor({id, node, visible}: VertexPropertyColorProps) {
  if (!visible || !node) return null

  const [showInput, setShowInput] = useState(false)
  const [nodeColor, setNodeColor] = useState(node?.style?.backgroundColor)

  const updateNodeStyle = useFlowContext((s) => s.updateNodeStyle);

  const changeNodeStyle = useCallback(
    (properties: React.CSSProperties) => {
      updateNodeStyle(id, properties);
    },
    [id]
  );

  return (
    <>
      {
        !showInput &&
        <button onClick={() => {setShowInput(true)}}>
          color
        </button>
      }
      {
        !!showInput &&
        <input
          type="color"
          value={ nodeColor }
          onChange={(e) => {
            setNodeColor(e.target.value)
            changeNodeStyle({ backgroundColor: nodeColor, color: getContrastColor(nodeColor)})
          }}
        />
      }
    </>
  )
}

function getContrastColor(hexColor: string): string {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hexColor);
  const rgb = result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;

  if (!rgb) {
    return "#000000";
  }

  const yiq = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;

  return yiq >= 128 ? "#000000" : "#ffffff";
}