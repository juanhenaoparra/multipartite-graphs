import { GenRandomHex } from "@/shared/id";
import React, { useCallback } from "react";
import { Panel } from "reactflow";
import { GetNodeStyle, ParseGraph } from "../api/binding";
import { RunCheckBipartite, RunStrategy } from "../api/api";
import { useFlowContext } from "@/store/store";
import NewIcon  from '@/assets/new_icon.svg?react';
import DownloadIcon  from '@/assets/download_icon.svg?react';
import UploadIcon  from '@/assets/upload_icon.svg?react';
import SaveIcon  from '@/assets/save_icon.svg?react';
import RunIcon  from '@/assets/run_icon.svg?react';

const defaultNodeRadius = 1

export default function ToolsPanel({}) {
  const [graphId, nodes, addNodes, graphExport, saveGraph, setNodes, setEdges, doReload] = useFlowContext((s) => [s.id, s.nodes, s.addNodes, s.export, s.save, s.setNodes, s.setEdges, s.doReload])

  const onAdd = useCallback(() => {
    const newNode = {
      id: GenRandomHex(8),
      type: 'vertex',
      data: {
        label: 'My new node',
        backgroundColor: '#efefef',
        color: '#000000',
        radius: defaultNodeRadius,
      },
      position: {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight
      },
      style: GetNodeStyle({radius: defaultNodeRadius, backgroundColor: '#efefef'}),
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

  const onImport = useCallback(() => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (event) => {
      const file = (event.target as HTMLInputElement).files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        let graph = JSON.parse(e.target.result as string);
        graph = ParseGraph(graph)

        setNodes(graph.initialNodes)
        setEdges(graph.initialEdges)
      }
      reader.readAsText(file);
    }
    input.click();
  }, [nodes])

  const onSave = useCallback(() => {
    saveGraph()
  }, [nodes])

  const onRunCheckBipartite = useCallback(() => {
    saveGraph().then(() => {
      RunCheckBipartite(graphId).then((res) => {
        if (res.isBipartite == false) {
          alert(`Checking bipartiteness: ${res.reason}`)
        }

        doReload()
      })
    })
  }, [graphId])

  const onRunStrategy = useCallback((strategy_number: string) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (event) => {
      const file = (event.target as HTMLInputElement).files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        let jsonFile = JSON.parse(e.target.result as string);
        RunStrategy(strategy_number, jsonFile).then((res) => {
          console.log(`Strategy#${strategy_number} Response:`, res)
          if (!res.graph) {
            return
          }

          const receivedGraph = ParseGraph(res.graph)
          setNodes(receivedGraph.initialNodes)
          setEdges(receivedGraph.initialEdges)
        }).catch((err) => {
          alert(`Error: ${err}`)
        })
      }

      reader.readAsText(file);
    }
    input.click();
  }, [nodes])

  return (
    <Panel position="top-left" className="main-panel">
      <button onClick={onAdd}>
        <NewIcon/>
        add
      </button>
      <button onClick={onImport}>
        <UploadIcon/>
        import
      </button>
      <button onClick={onExport}>
        <DownloadIcon/>
        export
      </button>
      <button onClick={onSave}>
        <SaveIcon/>
        save
      </button>
      <button className="run-icon" onClick={onRunCheckBipartite}>
        <RunIcon/>
        bipartite
      </button>
      <button className="run-icon" onClick={() => onRunStrategy('1')}>
        <RunIcon/>
        strategy#1
      </button>
      <button className="run-icon" onClick={() => onRunStrategy('2')}>
        <RunIcon/>
        strategy#2
      </button>
      <button className="run-icon" onClick={() => onRunStrategy('3')}>
        <RunIcon/>
        strategy#3
      </button>
    </Panel>
  )
}