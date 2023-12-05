import React, { useState, useCallback } from "react";
import "./Registration.raw.scss";
import Header from "components/Header/Header";
import { Link } from "react-router-dom";

interface UserData {
  userEmail: string;
  userName: string;
  firstName: string;
  lastName: string;
  stadt: string;
  plz: string;
  street: string;
  phone: string;
}

interface RegistrationProps {
  onContinue: () => void;
  userData: UserData;
  updateUserData: (newData: Partial<UserData>) => void;
}

const Registration: React.FC<RegistrationProps & { onCreateAccountSuccess: (accountId: number) => void }> = ({
  onContinue,
  userData,
  updateUserData,
  onCreateAccountSuccess
}) => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [usernameError, setUsernameError] = useState("");
  const [emailError, setEmailError] = useState("");

  // Debounce-Funktion
  const debounce = (func, delay) => {
    let inDebounce;
    return function(...args) {
      clearTimeout(inDebounce);
      inDebounce = setTimeout(() => func(...args), delay);
    };
  };

  const checkUsernameAvailability = useCallback(
    debounce((username) => {
      fetch(`http://localhost:8000/check-username/${username}`)
        .then((res) => res.json())
        .then((data) => {
          setUsernameError(data.username_exists ? "Benutzername ist bereits vergeben." : "");
        });
    }, 500),
    []
  );

  const checkEmailAvailability = useCallback(
    debounce((email) => {
      fetch(`http://localhost:8000/check-email/${email}`)
        .then((res) => res.json())
        .then((data) => {
          setEmailError(data.email_exists ? "E-Mail ist bereits vergeben." : "");
        });
    }, 500),
    []
  );
  const createAccount = async (userData, password) => {
    const response = await fetch('http://localhost:8000/account/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: userData.userName,
        email: userData.userEmail,
        password: password,
      }),
    });
  
    if (!response.ok) {
      throw new Error('Fehler beim Erstellen des Accounts');
    }
  
    return response.json();
  };  

  const handleUsernameChange = (e) => {
    const newUsername = e.target.value;
    updateUserData({ ...userData, userName: newUsername });
    checkUsernameAvailability(newUsername);
  };

  const handleEmailChange = (e) => {
    const newEmail = e.target.value;
    updateUserData({ ...userData, userEmail: newEmail });
    checkEmailAvailability(newEmail);
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
  
    if (password !== confirmPassword) {
      setPasswordError("Passwörter stimmen nicht überein.");
      return;
    }
    setPasswordError("");
  
    if (usernameError || emailError) {
      // Anzeigen weiterer Fehlermeldungen, falls nötig
      return;
    }
  
    try {
      const accountData = await createAccount(userData, password);
      onCreateAccountSuccess(accountData.id); // Nehmen Sie an, dass die Account-ID zurückgegeben wird
      console.log(accountData); // Für Debugging-Zwecke
      onContinue(); // Weiterleitung oder nächster Schritt im UI-Flow
    } catch (error) {
      console.error(error);
      // Setzen Sie hier eine Fehlermeldung, um dem Benutzer Feedback zu geben
    }
  };
  

  return (
    <div className="registration-wrapper">
      <div className="background-image"></div>
      <main className="registration-container">
        <Header />
        <div className="registration-form">
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlFor="username">Benutzername *</label>
              <input
                required
                type="text"
                id="username"
                value={userData.userName}
                onChange={handleUsernameChange}
              />
              {usernameError && <p className="error">{usernameError}</p>}
            </div>
            <div>
              <label htmlFor="useremail">E-Mail *</label>
              <input
                required
                type="email"
                id="useremail"
                value={userData.userEmail}
                onChange={handleEmailChange}
              />
              {emailError && <p className="error">{emailError}</p>}
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
              <button type="submit" disabled={!!usernameError || !!emailError}>Erstellen</button>
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
