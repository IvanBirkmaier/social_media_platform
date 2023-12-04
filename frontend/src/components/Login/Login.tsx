import React, { useState } from "react";
import "./Login.raw.scss";
import Header from "components/Header/Header";

import { Link } from "react-router-dom";

const LoginForm: React.FC<{ onLoginSuccess: () => void }> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [usernameError, setUsernameError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const isUsernameEmpty = !username;
    const isPasswordEmpty = !password;

    setUsernameError(isUsernameEmpty);
    setPasswordError(isPasswordEmpty);

    if (!isUsernameEmpty && !isPasswordEmpty) {
      console.log(username, password);
      onLoginSuccess();
    }
  };

  const errorStyle = {
    borderColor: "red",
    boxShadow: "0 0 5px red",
  };
  const getStyle = (hasError: boolean) => (hasError ? errorStyle : {});

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
                style={getStyle(usernameError)}
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
                style={getStyle(passwordError)}
              />
            </div>
            <div className="button-wrapper">
              <button type="submit">Weiter</button>
            </div>
          </form>
          <p className="forgotpwd-text">
            <Link to="/requestpassword"> Passwort vergessen? </Link>
          </p>
          <p className="text">
            Sie haben noch keinen Account?{" "}
            <Link to="/registration"> Hier Registrieren </Link>
          </p>
        </div>
      </main>
    </div>
  );
};

export default LoginForm;
