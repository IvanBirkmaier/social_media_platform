import React from "react";
import "./RegistrationInformation.raw.scss";
import Header from "../Header/Header";
import { useNavigate } from "react-router-dom"; // Änderung hier

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

interface RegistrationInformationProps {
  userData: UserData;
  updateUserData: (newData: Partial<UserData>) => void;
  onBack: () => void;
  onSubmitSuccess: () => void;
}

const RegistrationInformation: React.FC<
  RegistrationInformationProps & { accountId: number }
> = ({ userData, updateUserData, onSubmitSuccess, accountId }) => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const navigate = useNavigate(); // Änderung hier
  const handleSkip = () => {
    navigate("/"); // Weiterleitung zur /home-Route
  };
  const createProfile = async () => {
    try {
      const response = await fetch(`${backendUrl}/profile/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          account_id: accountId,
          vorname: userData.firstName,
          nachname: userData.lastName,
          city: userData.stadt,
          plz: userData.plz,
          street: userData.street,
          phone_number: userData.phone,
        }),
      });

      if (!response.ok) {
        throw new Error("Fehler beim Erstellen des Profils");
      }

      return response.json();
    } catch (error) {
      console.error(error);
      // Setzen Sie hier eine Fehlermeldung, um dem Benutzer Feedback zu geben
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const profileData = await createProfile();
    console.log(profileData); // Für Debugging-Zwecke
    onSubmitSuccess();
  };
  return (
    <div className="registration-info-wrapper">
      <div className="background-image"></div>
      <main className="registration-info-container">
        <Header />
        <div className="registration-info-form">
          <form onSubmit={handleSubmit}>
            <div className="username-wrapper">
              <div>
                <label htmlFor="firstname">Vorname *</label>
                <input
                  type="text"
                  id="firstname"
                  value={userData.firstName}
                  onChange={(e) =>
                    updateUserData({ firstName: e.target.value })
                  }
                />
              </div>
              <div>
                <label htmlFor="lastname">Nachname *</label>
                <input
                  type="text"
                  id="lastname"
                  value={userData.lastName}
                  onChange={(e) => updateUserData({ lastName: e.target.value })}
                />
              </div>
            </div>
            <div className="username-wrapper">
              <div>
                <label htmlFor="city">Stadt </label>
                <input
                  type="text"
                  id="city"
                  value={userData.stadt}
                  onChange={(e) => updateUserData({ stadt: e.target.value })}
                />
              </div>
              <div>
                <label htmlFor="plz">Postleitzahl</label>
                <input
                  type="number"
                  id="plz"
                  value={userData.plz}
                  onChange={(e) => updateUserData({ plz: e.target.value })}
                />
              </div>
            </div>
            <div>
              <label htmlFor="street">Straße und Hausnummer</label>
              <input
                type="text"
                id="street"
                value={userData.street}
                onChange={(e) => updateUserData({ street: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="phone">Telefonnummer</label>
              <input
                type="text"
                id="phone"
                value={userData.phone}
                onChange={(e) => updateUserData({ phone: e.target.value })}
              />
            </div>
            <div className="checkbox-wrapper">
              <input type="checkbox" id="datenschutz" required />
              <label htmlFor="datenschutz">Datenschutz</label>
            </div>
            <div className="button-wrapper">
              <button
                type="button"
                onClick={handleSkip}
                className="button-secondary"
              >
                Überspringen
              </button>
              <button type="submit">Weiter</button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default RegistrationInformation;
