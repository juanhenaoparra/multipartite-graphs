import { GenRandomHex } from "@/shared/id"
import React, { useCallback, useState } from "react"
import { Link, useNavigate } from "react-router-dom"

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

  const handleSubmit = (e) => {
    e.preventDefault()

    if (random) {
      alert('Random flow not implemented yet')
      return
    }

    const flowId = GenRandomHex(8)
    navigate(`/graphs/${flowId}`)
  }

  return (
    <>
      <h1>New Flow</h1>
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
            <input type="number" name="num-nodes-number" defaultValue="100"/>
          </div>}
          { random &&
          <div>
            <label htmlFor="slc-graph-type">Graph Type</label>
            <select name="slc-graph-type" defaultValue="">
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
            <select name="slc-graph-direction" defaultValue="">
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
              <input type="checkbox" name="is-weighted" />
          </div>}
          { random && <div>
              <label htmlFor="is-connected">Is Connected</label>
              <input type="checkbox" name="is-connected" />
          </div>}
          { random && <div>
              <label htmlFor="is-complete">Is Complete</label>
              <input type="checkbox" name="is-complete" />
          </div>}

          <button
            type="submit"
          >New</button>
        </form>
      </div>
    </>
  )
}