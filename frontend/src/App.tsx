import { Route, Routes } from "react-router-dom";
import RegistrationSuccess from "components/RegistrationSuccess/RegistrationSuccess";
import ResetPassword from "components/ResetPassword/ResetPassword";
import RegistrationParent from "components/RegistrationParent/RegistrationParent";
import LoginParent from "components/LoginParent/LoginParent";
import RequestPassword from "components/RequestPassword/RequestPassword";

const App: React.FC = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<LoginParent />} />
        <Route path="/registration" element={<RegistrationParent />} />
        <Route path="/registrationsuccess" element={<RegistrationSuccess />} />
        <Route path="/resetpassword" element={<ResetPassword />} />
        <Route path="/requestpassword" element={<RequestPassword />} />
      </Routes>
    </>
  );
};

export default App;
