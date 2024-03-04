/// <reference types="vite-plugin-svgr/client" />

import React from 'react';
import { NavbarItemsData } from './NavbarItems'
import MenuItems from './MenuItems';
import Logo  from '../assets/logo.svg?react';

import './Navbar.css';

const Navbar = () => {
  return (
    <div className="navbar">
      <div style={{marginInline: "10px"}}>
        <Logo fill='white' width="60px"/>
      </div>
      <nav className="desktop-nav">
        <ul className='menus'>
          {NavbarItemsData.map((menu, index) => {
            return <MenuItems items={menu} key={index} />
          })}
        </ul>
      </nav>
    </div >
  );
};

export default Navbar;
