import RegistrationSuccess from "../RegistrationSuccess/RegistrationSuccess";
import { useState } from "react";
import Registration from "../Registration/Registration";
import RegistrationInformation from "../RegistrationInformation/RegistrationInformation";
import { useAuth } from "../Auth/AuthContext";

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
const RegistrationParent: React.FC = () => {
  const [step, setStep] = useState(1);
  const [userData, setUserData] = useState({
    userEmail: "",
    userName: "",
    firstName: "",
    lastName: "",
    stadt: "",
    plz: "",
    street: "",
    phone: "",
  });
  const { login } = useAuth();

  const goToNextStep = () => {
    setStep(step + 1);
  };

  const goToPreviousStep = () => {
    setStep(step - 1);
  };

  const updateUserData = (newData: Partial<UserData>) => {
    setUserData({ ...userData, ...newData });
  };

  const handleSubmitSuccess = () => {
    setStep(3);
  };

  const [accountId, setAccountId] = useState(-1);

  const handleCreateAccountSuccess = (accountId: number) => {
    setAccountId(accountId);
    login({ id: accountId, username: userData.userName });
    goToNextStep();
  };

  return (
    <div>
      {step === 1 && (
        <Registration
          onCreateAccountSuccess={handleCreateAccountSuccess}
          onContinue={goToNextStep}
          userData={userData}
          updateUserData={updateUserData}
        />
      )}
      {step === 2 && (
        <RegistrationInformation
          accountId={accountId}
          userData={userData}
          updateUserData={updateUserData}
          onBack={goToPreviousStep}
          onSubmitSuccess={handleSubmitSuccess}
        />
      )}
      {step === 3 && <RegistrationSuccess />}
    </div>
  );
};

export default RegistrationParent;
