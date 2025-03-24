import React from "react";
import {  Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "./components copy/Navbar/Navbar";
import Sidebar from "./components copy/Sidebar/Sidebar";
import Add from "./pages/Add/Add";
import Addjob from "./pages/Addjob/Addjob";


const App = () => {

  const url = "http://127.0.0.1:8000";

  return (
    <div>
      <ToastContainer />
      <Navbar />
      <hr/>
      <div className="app-content">
        <Sidebar />
        <Routes>
          <Route path="/Addresume" element ={<Add url={url}/>}/>
          <Route path="/Addjob" element ={<Addjob url={url}/>}/>
          <Route path="/Listresume" element ={<Add url={url}/>}/>
          <Route path="/Listjob" element ={<Add url={url}/>}/>
        </Routes>
      </div>  
    </div>    
  )
}

export default App;