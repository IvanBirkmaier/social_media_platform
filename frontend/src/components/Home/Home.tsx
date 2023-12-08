import React, { useState } from "react";
import "./Home.raw.scss";
import Header from "components/Header/Header";
import { Link, useNavigate } from "react-router-dom";
const Home: React.FC = () => {
  return (
    <div className="home-wrapper">
      <div className="background-image"></div>
      <main className="home-container">
      <Header />
      {/*profile-container muss dann ein eingene Componente werden */}
      <div className="profile-container">
        <div className="profile-container-section-profile">
          <div className="profile-picture">
          </div>
          {/*Hier muss ein State oder irgendwas übergeben werden um den Benutzername zu setzen muss dann ein eingene Componente werden */}
          <p className="username-text">Benutzername</p>
        </div>
        <div className="profile-container-section-information">
          <div className="profile-container-section-information-content">
            <p className="username-text">Profil beschreibung BLABLABLABLA</p>
            <p className="username-text">Profil bearbeiten</p>
          </div>
        </div>
      </div>
      {/*navigation-container muss dann ein eingene Componente werden */}
      <div className="navigation-container">

      </div>
      <div className="posts-container">
         {/*Post-container muss dann ein eingene Componente werden */}
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
      
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        <div className="post-container">

        </div>
        
      </div>
      </main>
    </div>
  );
};

export default Home;
