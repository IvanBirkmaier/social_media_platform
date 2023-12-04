import React, { useState } from "react";
import "./Registration.raw.scss";
import Header from "components/Header/Header";
import { Link } from "react-router-dom";

interface UserData {
  userEmail: string;
  firstName: string;
  lastName: string;
  role: string;
  institutionName: string;
  schoolNumber: string;
}

interface RegistrationProps {
  onContinue: () => void;
  userData: UserData;
  updateUserData: (newData: Partial<UserData>) => void;
}

const Registration: React.FC<RegistrationProps> = ({
  onContinue,
  userData,
  updateUserData,
}) => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setPasswordError("Passwörter stimmen nicht überein.");
      return;
    }
    setPasswordError("");
    console.log(userData.userEmail, password);
    onContinue();
  };

  return (
    <div className="registration-wrapper">
      <div className="background-image"></div>
      <main className="registration-container">
        <Header />
        <div className="registration-form">
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="useremail">E-mail *</label>
              <input
                required
                type="email"
                id="useremail"
                value={userData.userEmail}
                onChange={(e) => updateUserData({ userEmail: e.target.value })}
              />
            </div>
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
              <label htmlFor="confirmpassword">Passwort wiederholen *</label>
              <input
                required
                type="password"
                id="confirmpassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              {passwordError && <p className="error">{passwordError}</p>}
            </div>
            <div className="button-wrapper">
              <button type="submit">Speichern</button>
            </div>
            <p className="text">
              Sie haben bereits einen Account? <Link to="/">Zum Login</Link>
            </p>
          </form>
        </div>
      </main>
    </div>
  );
};

export default Registration;
