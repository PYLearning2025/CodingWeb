import { Routes, Route } from 'react-router-dom';
import Head from './head/head';
import Home from './router/home/home';
import About from './router/about/about';
import Login from './router/login/login';
import Register from './router/register/register';
import './App.css';

function App() {
  return (
    <div className="App">
      {/* Head 會一直顯示在最上方 */}
      <Head />
      
      {/* 這裡的內容會根據網址改變 */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </div>
  );
}

export default App;
