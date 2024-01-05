import { Route, Routes } from "react-router-dom";
import RegistrationSuccess from "./components/RegistrationSuccess/RegistrationSuccess";
import ResetPassword from "./components/ResetPassword/ResetPassword";
import RegistrationParent from "./components/RegistrationParent/RegistrationParent";
import LoginParent from "./components/LoginParent/LoginParent";
import RequestPassword from "./components/RequestPassword/RequestPassword";
import RootLayout from "./components/_root/RootLayout";
import { Home, AddPost } from "./components/_root/pages";
import "./index.css";

const App = () => {
  return (
    <main>
      <Routes>
        {/* public routes */}
        <Route path="/login" element={<LoginParent />} />
        <Route path="/registration" element={<RegistrationParent />} />
        <Route path="/registrationsuccess" element={<RegistrationSuccess />} />
        <Route path="/resetpassword" element={<ResetPassword />} />
        <Route path="/requestpassword" element={<RequestPassword />} />
        {/* private routes */}
        <Route element={<RootLayout />}>
          <Route index element={<Home />} />
          <Route path="/addPost" element={<AddPost />} />
        </Route>
      </Routes>
    </main>
  );
};

export default App;
