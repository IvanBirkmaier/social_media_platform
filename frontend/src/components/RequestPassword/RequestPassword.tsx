import React, { useState } from "react";
import Header from "../Header/Header";
import { Link } from "react-router-dom";

const RequestPassword: React.FC = () => {
  const [userEmail, setUserEmail] = useState("");
 

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log(userEmail);
  };

  return (
    <div className="forgotpwd-wrapper">
      <div className="background-image"></div>
      <main className="forgotpwd-container">
        <Header />
        <div className="forgotpwd-form">
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="useremail">E-mail *</label>
              <input
                required
                type="email"
                id="useremail"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
              />
            </div>
           
            <div className="button-wrapper">
              <button type="submit">Senden</button>
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

export default RequestPassword;