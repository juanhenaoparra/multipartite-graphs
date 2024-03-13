import { useFlowContext } from "@/store/store";
import React, { useCallback } from "react"

export default function EdgeContextMenu({id, color, weight, lineType}) {
  const [updateEdgeData] = useFlowContext((s) => [s.updateEdgeData]);

  const updateEdgeColor = useCallback((e) => {
    if (!e || !e.target) return

    updateEdgeData(id, {color: e.target.value})
  }, [id]);

  const updateLineType = useCallback((e) => {
    if (e.target.value === '' || e.target.value === 'continue') {
      updateEdgeData(id, {lineType: "continue"});
      return
    }

    updateEdgeData(id, {lineType: "dashed"});
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
      <input type="color" id="edge-color-selector" defaultValue={color} onChange={updateEdgeColor}/>
      <select id="edge-line_type-selector" onChange={updateLineType} value={lineType}>
        <option value="continue">Continue</option>
        <option value="dashed">Dashed</option>
      </select>
    </div>
  )
}