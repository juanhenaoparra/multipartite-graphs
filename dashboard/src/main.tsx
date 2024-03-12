import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom"

import Home from '@/routes/Home/Home'
import Flow from '@/routes/Graphs/Flow'
import Layout from '@/routes/Layout'
import './index.css'
import NewFlow from './routes/Graphs/NewFlow'
import OpenFlow from './routes/Graphs/OpenFlow'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        path: "/graphs/new",
        element: <NewFlow />
      },
      {
        path: "/graphs/open",
        element: <OpenFlow />
      },
      {
        path: "/graphs/:graphId",
        element: <Flow />
      }
    ]
  },
]);

const root = document.getElementById('root')!

ReactDOM.createRoot(root).render(
  <RouterProvider router={router}/>
)
