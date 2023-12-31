import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import LogIn from './components/LogIn'; 
import NewListing from'./components/NewListing';
import SignUp from './components/SignUp'; 
import AboutUs from './components/AboutUs';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/login" element={<LogIn />} />
      <Route path="/new-listing" element={<NewListing />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/about-us" element={<AboutUs />} />
    </Routes>
  </Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();