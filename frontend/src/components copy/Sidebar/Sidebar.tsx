import React from 'react'
import './Sidebar.css';
import { assets } from '../../assets/admin_assets/assets';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className='sidebar'>
        <div className="sidebar-options">
            <NavLink to= '/addresume' className="sidebar-option">
                <img src={assets.add_icon} alt=''/>
                <p>Add Resume</p>
            </NavLink>
            <NavLink to='/addjob'  className="sidebar-option">
                <img src={assets.add_icon} alt=''/>
                <p>Add Job Description</p>
            </NavLink>
            <NavLink to='/listresume'  className="sidebar-option">
                <img src={assets.order_icon} alt=''/>
                <p>List Resume</p>
            </NavLink>
            <NavLink to='/listjob'  className="sidebar-option">
                <img src={assets.order_icon} alt=''/>
                <p>List Job Description</p>
            </NavLink>
        </div>
    </div>
  )
}

export default Sidebar
