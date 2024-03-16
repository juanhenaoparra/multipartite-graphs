import { GenRandomHex } from "@/shared/id"
import React, { useCallback, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { GenRandomFlow, GenRandomFlowInput } from "./api/api"

const graphTypes = [
  "bipartite",
  "tripartite",
]

const graphDirections = [
  "directed",
  "undirected",
]

const edgeTypes = [
  "weighted",
  "unweighted",
]

function capitalize(string: string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export default function NewFlow({}) {
  const navigate = useNavigate()
  const [random, setRandom] = useState(false)
  const [nodesNumber, setNodesNumber] = useState(100)
  const [graphType, setGraphType] = useState("")
  const [graphDirection, setGraphDirection] = useState("")
  const [isWeighted, setIsWeighted] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isComplete, setIsComplete] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()

    if (random) {
      const input: GenRandomFlowInput = {
        nodesNumber,
        graphType,
        direction: graphDirection,
        weighted: isWeighted,
        connected: isConnected,
        complete: isComplete,
        probability: 0.5,
        degree: 2,
      }

      GenRandomFlow(input).then((flow) => {
        navigate(`/graphs/${flow.name}`)
      }).catch((error) => {
        alert("Error generating random graph, please check the api connection: " + error)
      })

      return
    }

    const flowId = GenRandomHex(8)
    navigate(`/graphs/${flowId}`)
  }

  return (
    <>
      <h1>New Graph</h1>
      <div className="container">
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="chk-random">Random</label>
            <input
              type="checkbox"
              name="chk-random"
              checked={random}
              onChange={(e) => setRandom(e.target.checked)}
            />
          </div>
          { random && <div>
            <label htmlFor="num-nodes-number">Number of nodes</label>
            <input
              type="number"
              name="num-nodes-number"
              defaultValue="100"
              value={nodesNumber}
              onChange={(e) => setNodesNumber(parseInt(e.target.value))}
            />
          </div>}
          { random &&
          <div>
            <label htmlFor="slc-graph-type">Graph Type</label>
            <select
              name="slc-graph-type"
              defaultValue=""
              value={graphType}
              onChange={(e) => setGraphType(e.target.value)}
            >
            <option value="">Select one</option>
              {
                graphTypes.map((type) => (
                  <option key={type} value={type}>{capitalize(type)}</option>
                ))
              }
            </select>
          </div>}
          { random && <div>
            <label htmlFor="slc-graph-direction">Graph Direction</label>
            <select
              name="slc-graph-direction"
              defaultValue=""
              value={graphDirection}
              onChange={(e) => setGraphDirection(e.target.value)}
            >
              <option value="">Select one</option>
              {
                graphDirections.map((direction) => (
                  <option key={direction} value={direction}>{capitalize(direction)}</option>
                ))
              }
            </select>
          </div>}
          { random && <div>
              <label htmlFor="is-weighted">Is Weighted</label>
              <input
                type="checkbox"
                name="is-weighted"
                checked={isWeighted}
                onChange={(e) => setIsWeighted(e.target.checked)}
              />
          </div>}
          { random && <div>
              <label htmlFor="is-connected">Is Connected</label>
              <input
                type="checkbox"
                name="is-connected"
                checked={isConnected}
                onChange={(e) => setIsConnected(e.target.checked)}
              />
          </div>}
          { random && <div>
              <label htmlFor="is-complete">Is Complete</label>
              <input
                type="checkbox"
                name="is-complete"
                checked={isComplete}
                onChange={(e) => setIsComplete(e.target.checked)}
              />
          </div>}

          <button
            type="submit"
          >New</button>
        </form>
      </div>
    </>
  )
}