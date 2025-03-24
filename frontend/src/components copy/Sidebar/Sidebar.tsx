import React from 'react'
import './Sidebar.css';
import { assets } from '../../assets/admin_assets/assets';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className='sidebar'>
        <div className="sidebar-options">
            <NavLink to= '/Addresume' className="sidebar-option">
                <img src={assets.add_icon} alt=''/>
                <p>Add Resume</p>
            </NavLink>
            <NavLink to='/Addjob'  className="sidebar-option">
                <img src={assets.add_icon} alt=''/>
                <p>Add Job Description</p>
            </NavLink>
            <NavLink to='/Listresume'  className="sidebar-option">
                <img src={assets.order_icon} alt=''/>
                <p>List Resume</p>
            </NavLink>
            <NavLink to='/Listjob'  className="sidebar-option">
                <img src={assets.order_icon} alt=''/>
                <p>List Job Description</p>
            </NavLink>
        </div>
    </div>
  )
}

export default Sidebar
