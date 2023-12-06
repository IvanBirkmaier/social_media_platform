import { Route, Routes } from "react-router-dom";
import RegistrationSuccess from "components/RegistrationSuccess/RegistrationSuccess";
import ResetPassword from "components/ResetPassword/ResetPassword";
import RegistrationParent from "components/RegistrationParent/RegistrationParent";
import LoginParent from "components/LoginParent/LoginParent";
import RequestPassword from "components/RequestPassword/RequestPassword";
import Home from "components/Home/Home";


const App: React.FC = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<LoginParent />} />
        <Route path="/registration" element={<RegistrationParent />} />
        <Route path="/registrationsuccess" element={<RegistrationSuccess />} />
        <Route path="/resetpassword" element={<ResetPassword />} />
        <Route path="/requestpassword" element={<RequestPassword />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </>
  );
};

export default App;
