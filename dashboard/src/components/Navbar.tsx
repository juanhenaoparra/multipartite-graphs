import React from 'react';
import { NavbarItemsData } from './NavbarItems'
import MenuItems from './MenuItems';

import './Navbar.css';

const Navbar = () => {
  return (
    <div className="navbar">
      <div>
        <img src='/logo.svg'/>
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
