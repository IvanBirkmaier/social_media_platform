import { Route, Routes } from "react-router-dom";
import RegistrationSuccess from "./components/RegistrationSuccess/RegistrationSuccess";
import ResetPassword from "./components/ResetPassword/ResetPassword";
import RegistrationParent from "./components/RegistrationParent/RegistrationParent";
import LoginParent from "./components/LoginParent/LoginParent";
import RequestPassword from "./components/RequestPassword/RequestPassword";
import RootLayout from "./components/_root/RootLayout";
import { Feed, AddPost, Home } from "./components/_root/pages";
import { AuthProvider } from "./components/Auth/AuthContext";
import "./index.css";

const App = () => {
  return (
    <main>
      <AuthProvider>
        <Routes>
          {/* public routes */}
          <Route index element={<LoginParent />} />
          <Route path="/registration" element={<RegistrationParent />} />
          <Route
            path="/registrationsuccess"
            element={<RegistrationSuccess />}
          />
          <Route path="/resetpassword" element={<ResetPassword />} />
          <Route path="/requestpassword" element={<RequestPassword />} />
          {/* private routes */}
          <Route element={<RootLayout />}>
            <Route path="/feed" element={<Feed />} />
            <Route path="/addPost" element={<AddPost />} />
            <Route path="/home" element={<Home />} />
          </Route>
        </Routes>
      </AuthProvider>
    </main>
  );
};

export default App;
