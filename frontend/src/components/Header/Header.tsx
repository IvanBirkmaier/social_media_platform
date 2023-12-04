import React from "react";
import logo from "assets/befake-logo.svg";
import "./Header.raw.scss";

const Header: React.FC = () => {
  return (
    <header className="login-modal-head">
      <img src={logo} alt="Logo" className="logo" />
    </header>
  );
};

export default Header;
