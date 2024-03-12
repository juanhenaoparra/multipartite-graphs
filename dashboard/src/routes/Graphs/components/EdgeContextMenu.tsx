import { useFlowContext } from "@/store/store";
import React, { useCallback } from "react"

export default function EdgeContextMenu({id, color, weight}) {
  const [updateEdgeStyle, updateEdgeData] = useFlowContext((s) => [s.updateEdgeStyle, s.updateEdgeData]);

  const updateStyle = useCallback((e) => {
    updateEdgeStyle(id, {stroke: e.target.value});
  }, [id]);

  const updateWeight = useCallback((e) => {
    if (!e || !e.target) return
    updateEdgeData(id, {weight: e.target.value});
  }, [id])

  return (
    <div
      className="context-menu-container"
    >
      <input
        type="range"
        id="edge-weight-slider"
        defaultValue={weight}
        onChange={updateWeight}
        min={0}
        max={1}
        step={0.01}
      />
      <input type="color" id="edge-color-selector" defaultValue={color} onChange={updateStyle}/>
    </div>
  )
}