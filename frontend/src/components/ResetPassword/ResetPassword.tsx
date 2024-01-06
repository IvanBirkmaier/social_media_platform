import React, { useState } from "react";
import "./ResetPassword.raw.scss";
import Header from "../Header/Header";
import { Link } from "react-router-dom";

const ResetPassword: React.FC = () => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log(confirmPassword, password);
  };

  return (
    <div className="forgotpwd-wrapper">
      <div className="background-image"></div>
      <main className="forgotpwd-container">
        <Header />
        <div className="forgotpwd-form">
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="password">Passwort *</label>
              <input
                required
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password">Passwort wiederholen *</label>
              <input
                required
                type="password"
                id="confirmpassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
            <div className="button-wrapper">
              <button type="submit">Speichern</button>
            </div>
          </form>
          <p className="text">
            Sie haben bereits einen Account? <Link to="/">Zum Login</Link>
          </p>
        </div>
      </main>
    </div>
  );
};

export default ResetPassword;
