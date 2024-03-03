import React, { useState, useEffect, useRef, MutableRefObject } from 'react';
import Dropdown from './Dropdown';
import { NavLink } from 'react-router-dom';

const MenuItems = ({ items }) => {
  const [dropdown, setDropdown] = useState(false);
  let ref = useRef<HTMLLIElement>(null);

  useEffect(() => {
    const handler = (event: any) => {
    if (dropdown && ref.current && !ref.current.contains(event.target)) {
      setDropdown(false);
    }
  }

  document.addEventListener("mousedown", handler)
  document.addEventListener("touchstart", handler)

  return () => {
    document.removeEventListener("mousedown", handler)
    document.removeEventListener("touchstart", handler)
  }
  }, [dropdown]);

  return (
    <li className="menu-items" ref={ref}>
      {items.submenu ? (
        <>
          <button
            type="button"
            aria-haspopup="menu"
            aria-expanded={dropdown ? "true" : "false"}
            onClick={() => setDropdown((prev) => !prev)}
          >
            {items.title}{' '}
          </button>
          <Dropdown parent_path={items.url} submenus={items.submenu} dropdown={dropdown} />
        </>
      ) : (
        <NavLink to={items.url}>{items.title}</NavLink>
      )}
    </li>
  );
};

export default MenuItems;