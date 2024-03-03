import React from "react";
import { NavLink } from "react-router-dom";

const Dropdown = ({ parent_path, submenus, dropdown }) => {
  return (
    <ul className={`dropdown ${dropdown ? "show" : ""}`}>
      {submenus.map((submenu, index) => (
        <li key={index} className="menu-items">
          <NavLink to={`${parent_path}/${submenu.url}`}>{submenu.title}</NavLink>
        </li>
      ))}
    </ul>
  );
};

export default Dropdown;
