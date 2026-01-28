import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaHeartbeat, FaBars, FaTimes } from 'react-icons/fa';
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <FaHeartbeat className="logo-icon" />
          <span>Healthcare Analytics</span>
        </Link>

        <div className="menu-icon" onClick={toggleMenu}>
          {isOpen ? <FaTimes /> : <FaBars />}
        </div>

        <ul className={isOpen ? 'nav-menu active' : 'nav-menu'}>
          <li className="nav-item">
            <Link
              to="/"
              className={`nav-link ${isActive('/')}`}
              onClick={() => setIsOpen(false)}
            >
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link
              to="/upload"
              className={`nav-link ${isActive('/upload')}`}
              onClick={() => setIsOpen(false)}
            >
              Upload Data
            </Link>
          </li>
          <li className="nav-item">
            <Link
              to="/data-entry"
              className={`nav-link ${isActive('/data-entry')}`}
              onClick={() => setIsOpen(false)}
            >
              Data Entry
            </Link>
          </li>
          <li className="nav-item">
            <Link
              to="/dashboard"
              className={`nav-link ${isActive('/dashboard')}`}
              onClick={() => setIsOpen(false)}
            >
              Dashboard
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
