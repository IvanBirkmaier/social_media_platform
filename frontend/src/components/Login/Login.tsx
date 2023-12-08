import React, { useState } from "react";
import "./Login.raw.scss";
import Header from "components/Header/Header";
import { Link, useNavigate } from "react-router-dom";

const LoginForm: React.FC<{ onLoginSuccess: () => void }> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate(); // Hook um im Router zu navigieren

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!username || !password) {
      setErrorMessage('Bitte geben Sie Benutzername und Passwort ein.');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        onLoginSuccess(); // Sie können hier auch eine Weiterleitung einfügen
        console.log(response)
        navigate('/home'); // Weiterleitung zur Startseite nach dem Login
      } else {
        setErrorMessage(data.detail || 'Anmeldung fehlgeschlagen.');
      }
    } catch (error) {
      setErrorMessage('Netzwerkfehler oder Server nicht erreichbar.');
    }
  };

  return (
    <div className="login-wrapper">
      <div className="background-image"></div>
      <main className="login-container">
      <Header />
        <div className="login-form">
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="username">Benutzername *</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div>
              <label htmlFor="password">Passwort *</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="button-wrapper">
              <button type="submit">Weiter</button>
            </div>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
          </form>
          <p className="forgotpwd-text">
            <Link to="/requestpassword">Passwort vergessen?</Link>
          </p>
          <p className="text">
            Sie haben noch keinen Account?{" "}
            <Link to="/registration">Hier Registrieren</Link>
          </p>
        </div>
      </main>
    </div>
  );
};

export default LoginForm;
