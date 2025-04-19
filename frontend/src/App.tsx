import React from "react";
import {  Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "./components copy/Navbar/Navbar";
import Sidebar from "./components copy/Sidebar/Sidebar";
import Add from "./pages/Add/Add";
import Addjob from "./pages/Addjob/Addjob";
import Listresume from "./pages/Listresume/Listresume.tsx";
import Listjob from "./pages/ListJob/Listjob.tsx";

const App = () => {

  const url = "http://localhost:4000";

  return (
    <div>
      <ToastContainer />
      <Navbar />
      <hr/>
      <div className="app-content">
        <Sidebar />
        <Routes>
          <Route path="/addresume" element={<Add url={url} />} caseSensitive />
          <Route path="/addjob" element ={<Addjob url={url}/>} caseSensitive />
          {/* <Route path="/Listresume" element ={<Listresume url={url}/>}/>
          <Route path="/Listjob" element ={<Listjob url={url}/>}/> */}
        </Routes>
      </div>  
    </div>    
  )
}

export default App;