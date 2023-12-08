import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import "./RegistrationSucess.raw.scss";
import Header from "components/Header/Header";

const RegistrationSuccess: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/home');
    }, 1500);

    return () => clearTimeout(timer);
  }, [navigate]);

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
