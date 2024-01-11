import { useState } from "react";
import logo from "assets/befake-logo.svg";
import logout_svg from "assets/icons/logout.svg";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../ui/button";
import { useAuth } from "../Auth/AuthContext";
import deleteIcon from "assets/icons/delete.svg";
import { backendUrl } from "@/utils/utils";

const Topbar = () => {
  const navigate = useNavigate();
  const { logout, user } = useAuth();
  const [showConfirmationModal, setShowConfirmationModal] = useState(false);

  const handleLogout = () => {
    logout(); // Aufrufen der Logout-Funktion aus dem Authentifizierungskontext
    navigate("/"); // Weiterleitung zur Login-Seite
  };

  const openConfirmationModal = () => {
    setShowConfirmationModal(true);
  };

  const closeConfirmationModal = () => {
    setShowConfirmationModal(false);
  };

  const deleteAccount = async () => {
    try {
      const accountId = user?.id;
      const response = await fetch(`${backendUrl}/account/${accountId}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          // Fügen Sie hier weitere benötigte Header hinzu, z.B. für Authentifizierung
        },
      });

      if (!response.ok) {
        throw new Error("Fehler beim Löschen des Accounts");
      }

      // Account erfolgreich gelöscht
      console.log("Account erfolgreich gelöscht");
      logout(); // Benutzer ausloggen
      navigate("/"); // Weiterleitung zur Login-Seite
    } catch (error) {
      console.error("Fehler beim Löschen des Accounts:", error);
    }
  };

  const handleAccountDeletion = () => {
    deleteAccount();
    closeConfirmationModal();
    // Möglicherweise weitere Aktionen nach der Account-Löschung
  };

  return (
    <section className="topbar">
      <div className="flex-between py-4 px-5 h-28">
        <div>
          <img
            src={deleteIcon}
            alt="Delete"
            className="h-10 w-auto"
            onClick={openConfirmationModal}
          />
        </div>

        <Link to="/feed" className="flex items-center justify-center">
          <img
            src={logo}
            alt="Logo"
            className="h-15 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
          ></img>
        </Link>

        <Button variant="ghost" className="shad-button_ghost">
          <img
            src={logout_svg}
            alt="logout"
            className="h-10 w-auto"
            onClick={handleLogout}
          ></img>
        </Button>
      </div>

      {showConfirmationModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Do you really want to delete your account?</h3>
            <div className="modal-buttons">
              <button
                className="modal-button text-red"
                onClick={handleAccountDeletion}
              >
                Yes Delete
              </button>
              <button
                className="modal-button text-green-600"
                onClick={closeConfirmationModal}
              >
                No Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default Topbar;
