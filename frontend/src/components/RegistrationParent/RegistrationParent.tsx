import RegistrationSuccess from "components/RegistrationSuccess/RegistrationSuccess";
import { useState } from "react";
import Registration from "../Registration/Registration";
import RegistrationInformation from "../RegistrationInformation/RegistrationInformation";

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

  return (
    <div>
      {step === 1 && (
        <Registration
          onContinue={goToNextStep}
          userData={userData}
          updateUserData={updateUserData}
        />
      )}
      {step === 2 && (
        <RegistrationInformation
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
