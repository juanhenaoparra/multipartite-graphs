import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "@/components/Navbar";
import '@/routes/Root.css';

export default function Root() {
  return (
    <div style={{width: "100%"}}>
      <Navbar />
      <div className="container">
        <Outlet />
      </div>
    </div>
  );
}
