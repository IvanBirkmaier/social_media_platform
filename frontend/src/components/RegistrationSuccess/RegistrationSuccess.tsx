import React from "react";
import "./RegistrationSucess.raw.scss"
import Header from "components/Header/Header";

const RegistrationSuccess: React.FC = () => {
  return (
    <div className="registration-wrapper">
      <div className="background-image"></div>
      <main className="registration-container">
        <Header />
        <div className="registration-success">
          <p>
            Vielen Dank für Ihre Registrierung ❤️
          </p>
        </div>
      </main>
    </div>
  );
};

export default RegistrationSuccess;
