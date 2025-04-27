// App.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AboutPage from './AboutPage'; // 引入 AboutPage 组件
import RecipePage from './RecipePage'; // 你的功能页面
import './App.css';

function App() {
  return (

    <Routes>
      <Route path="/" element={<AboutPage />} /> {/* 默认的 About 页面 */}
      <Route path="/function" element={<RecipePage />} /> {/* 功能页面 */}
    </Routes>

  );
}

export default App;
