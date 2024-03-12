import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { GetFlow } from "./api/api"
import { ParseGraph } from "./api/binding"

export default function OpenFlow({}) {
  const navigate = useNavigate()
  const [graphId, setGraphId] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()

    GetFlow(graphId).then(() => {
      navigate(`/graphs/${graphId}`)
    }).catch((e) => {
      alert('Error fetching graph: ' + e)
    })
  }

  return (
    <>
      <h1>Open Graph</h1>
      <div className="container">
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="txt-graph-id">Graph ID</label>
            <input
              type="text"
              name="txt-graph-id"
              value={graphId}
              onChange={(e) => setGraphId(e.target.value)}
            />
          </div>

          <button
            type="submit"
          >Open</button>
        </form>
      </div>
    </>
  )
}