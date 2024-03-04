import React from 'react';
import Card from './components/Card';
import { NavbarItemsData } from '@/components/NavbarItems';

export default function Home() {
  return (
    <>
      <h1>Home</h1>
      <p>Here you can select how to start!</p>
      <div style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-around",
        gap: "10px",
        padding: "10px",
      }}>
        {NavbarItemsData.filter((el) => {
          return el.title !== "Home"
        }).map((menu, index) => {
          return <Card  title={menu.title}
                        description={menu.description}
                        color={menu.color}
                        path={menu.start_path || menu.url}
                        key={index} />
        })}
      </div>
    </>
  );
}