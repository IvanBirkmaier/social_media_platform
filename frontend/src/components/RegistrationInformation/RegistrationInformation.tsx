import React from "react";
import "./RegistrationInformation.raw.scss";
import Header from "components/Header/Header";

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

const RegistrationInformation: React.FC<RegistrationInformationProps> = ({
  userData,
  updateUserData,
  onBack,
  onSubmitSuccess,
}) => {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const jsonData = JSON.stringify(userData);
    console.log(userData);
    console.log("Form Data in JSON:", jsonData);
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
                  required
                />
              </div>
              <div>
                <label htmlFor="lastname">Nachname *</label>
                <input
                  type="text"
                  id="lastname"
                  value={userData.lastName}
                  onChange={(e) => updateUserData({ lastName: e.target.value })}
                  required
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
                  onChange={(e) =>
                    updateUserData({ stadt: e.target.value })
                  }
                  required
                />
              </div>
              <div>
                <label htmlFor="plz">Postleitzahl</label>
                <input
                  type="number"
                  id="plz"
                  value={userData.plz}
                  onChange={(e) => updateUserData({ plz: e.target.value })}
                  required
                />
              </div>
            </div>
            <div>
              <label htmlFor="street">Straße und Hausnummer</label>
              <input
                type="text"
                id="street"
                value={userData.street}
                onChange={(e) =>
                  updateUserData({ street: e.target.value })
                }
              />
            </div>
            <div>
              <label htmlFor="phone">Telefonnummer</label>
              <input
                type="number"
                id="phone"
                value={userData.phone}
                onChange={(e) => updateUserData({ phone: e.target.value })}
              />
            </div>
            <div className="checkbox-wrapper">
              <input type="checkbox" id="datenschutz" required/>
              <label htmlFor="datenschutz">Datenschutz</label>
            </div>
            <div className="button-wrapper">
              <button type="button" onClick={onBack} className="button-secondary">Zurück</button>
              <button type="submit">Weiter</button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default RegistrationInformation;
