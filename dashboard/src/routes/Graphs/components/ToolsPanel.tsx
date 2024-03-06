import { GenRandomHex } from "@/shared/id";
import React, { useCallback } from "react";
import { Panel } from "reactflow";
import { GetNodeStyle } from "../api/binding";
import { useFlowContext } from "@/store/store";
import NewIcon  from '@/assets/new_icon.svg?react';

export default function ToolsPanel({}) {
  const [nodes, addNodes] = useFlowContext((s) => [s.nodes, s.addNodes])

  const onAdd = useCallback(() => {
    const newNode = {
      id: GenRandomHex(8),
      type: 'vertex',
      data: { label: 'My new node', color: '#efefef' },
      position: {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      },
      style: GetNodeStyle({radius: 1, color: '#efefef'  }),
      className: 'vertex-circle'
    }

    addNodes([newNode])
  }, [nodes])

  return (
    <Panel position="top-left">
      <button onClick={onAdd} className="main-panel__button">
        <NewIcon/>
        add
      </button>
    </Panel>
  )
}