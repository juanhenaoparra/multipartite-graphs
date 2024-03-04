import React from "react"
import { useNavigate } from "react-router-dom"

export default function Card({title, description, color, path}: any) {
  const navigate = useNavigate()

  return (
    <button
      style={{
        backgroundColor: color || "#EDF6F9",
        color: "black",
        padding: "10px",
        width: "100%",
        maxWidth: "400px",
        height: "200px",
        fontWeight: "normal",
      }}
      onClick={() => navigate(path || "/")}
    >
      <h3>{title}</h3>
      <p style={{paddingInline: "70px"}}>{description}</p>
    </button>
  )
}