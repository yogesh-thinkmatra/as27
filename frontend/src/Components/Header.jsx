import React from "react";
import { Navbar } from "flowbite-react";
import { Link, Outlet } from "react-router-dom";
function Header() {
  return (
    <Navbar fluid rounded color="#000">
    <Navbar.Toggle />
    <Navbar.Collapse>
      <Link to="/" className="nav-link" activeClassName="active">
        Electricians
      </Link>
      <Link to="/sites" className="nav-link" activeClassName="active">
        Sites
      </Link>
    </Navbar.Collapse>
  </Navbar>
  );
}

export default Header;
