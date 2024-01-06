import React, { useEffect } from "react";
import logo from "assets/befake-logo.svg";
import logout_svg from "assets/icons/logout.svg";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../ui/button";
import { useAuth } from "../Auth/AuthContext";

const Topbar = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout(); // Aufrufen der Logout-Funktion aus dem Authentifizierungskontext
    navigate("/login"); // Weiterleitung zur Login-Seite
  };

  return (
    <section className="topbar">
      <div className="flex-between py-4 px-5 h-28">
        <Link to="/" className="flex items-center justify-center">
          <img
            src={logo}
            alt="Logo"
            className="h-15 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
          ></img>
        </Link>

        <Button variant="ghost" className="shad-button_ghost">
          <img
            src={logout_svg}
            alt="logout"
            className="h-10 w-auto"
            onClick={handleLogout}
          ></img>
        </Button>
      </div>
    </section>
  );
};

export default Topbar;
