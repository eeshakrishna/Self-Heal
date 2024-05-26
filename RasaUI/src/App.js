import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from './components/loginForm'
import Register from './components/registerForm'
import Start from './components/startPage'
import Home from './components/homePage'
import Chatbot from './components/Basic'
import OtherFeat from './components/otherFeat'
import Hotline from './components/hotLine'
import Sentimental from "./components/sentimental";

import './App.css';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Start/>} />
        <Route path="/home" element={<Home/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/chatbot" element={<Chatbot/>} />
        <Route path="/features" element={<OtherFeat/>} />
        <Route path="/hotline" element={<Hotline/>} />
        <Route path="/analyze_sentiment" element={<Sentimental/>}/>
      </Routes>
    </Router>
    
  );
};

export default App;