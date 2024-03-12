import { useFlowContext } from '@/store/store';
import React, { FC, useCallback, useEffect, useState } from 'react';
import { EdgeProps, getBezierPath, EdgeLabelRenderer, BaseEdge, BezierEdge, useKeyPress, useOnSelectionChange } from 'reactflow';
import EdgeContextMenu from './EdgeContextMenu';

const WeightEdge: FC<EdgeProps> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  style,
  markerEnd,
}) => {
  const escPressed = useKeyPress('Escape');

  useEffect(() => {
    if (escPressed) {
      setContextMenuData((prev) => ({ ...prev, visible: false }));
    }
  }, [escPressed]);

  useOnSelectionChange({
    onChange: () => {
      setContextMenuData((prev) => ({ ...prev, visible: false }));
    },
  });

  const [contextMenuData, setContextMenuData] = useState({
    visible: false,
    xClick: 0,
    yClick: 0,
    weight: 0,
  });

  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  return (
    <>
      <BaseEdge id={id} path={edgePath} markerEnd={markerEnd} style={style}/>
      <EdgeLabelRenderer>
        <div
          style={{
            position: 'absolute',
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY+10}px)`,
            padding: 10,
            borderRadius: 5,
            fontSize: 9,
            pointerEvents: 'all',
          }}
          className="nodrag nopan"
          onContextMenu={(e) => {
            e.preventDefault();
            setContextMenuData({
              visible: true,
              xClick: e.clientX,
              yClick: e.clientY,
              weight: data?.weight || 0
            });
          }}
        >
          <span>
            {data?.weight || 0}
          </span>
          {contextMenuData.visible &&
            <EdgeContextMenu
              id={id}
              color={style?.stroke}
              weight={contextMenuData.weight}
            />
          }
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default WeightEdge;
