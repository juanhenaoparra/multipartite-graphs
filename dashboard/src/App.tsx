import React from 'react';
import Flow from './flowbuilder/Flow';
import Navbar from './components/Navbar';

import './App.css';

export default function App() {
  return (
    <>
      <div className='container'>
        <div style={{ width: '85%', maxWidth: '85%', height: '100vh' }}>
          <Flow />
        </div>
      </div>
    </>
  );
}
