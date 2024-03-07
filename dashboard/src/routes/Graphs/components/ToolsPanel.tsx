import { GenRandomHex } from "@/shared/id";
import React, { useCallback } from "react";
import { Panel } from "reactflow";
import { GetNodeStyle } from "../api/binding";
import { useFlowContext } from "@/store/store";
import NewIcon  from '@/assets/new_icon.svg?react';
import DownloadIcon  from '@/assets/download_icon.svg?react';

export default function ToolsPanel({}) {
  const [nodes, addNodes, graphExport] = useFlowContext((s) => [s.nodes, s.addNodes, s.export])

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

  const onExport = useCallback(() => {
    const exportProperties = graphExport()
    let tempLink = document.createElement('a');
    tempLink.href = exportProperties.blobURL;
    tempLink.setAttribute('download', `${exportProperties.filename}.json`);
    tempLink.click();
  }, [nodes])

  return (
    <Panel position="top-left" className="main-panel">
      <button onClick={onAdd}>
        <NewIcon/>
        add
      </button>
      <button onClick={onExport}>
        <DownloadIcon/>
        export
      </button>
    </Panel>
  )
}