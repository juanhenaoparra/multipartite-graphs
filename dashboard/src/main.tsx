import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom"
import App from './App'
import Flow from './flowbuilder/Flow'
import './index.css'
import Root from '@/routes/Root'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "/graphs/:graphId",
        element: <Flow />
      }
    ]
  },
]);

const root = document.getElementById('root')!

ReactDOM.createRoot(root).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)
