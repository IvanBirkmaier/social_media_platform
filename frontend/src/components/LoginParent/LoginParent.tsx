import React, { useState } from "react";
import LoginForm from "../Login/Login";

const LoginParent: React.FC = () => {
  const [step, setStep] = useState(1);
  // const [userData, setUserData] = useState(dummyUserData);

  const handleLoginSuccess = () => {
    setStep(2); 
  };
  // const goToNextStep = () => {
  //   setStep(step + 1);
  // };

  // const goToPreviousStep = () => {
  //   setStep(step - 1);
  // };

  // const handleLoginMessage = () => {
  //   setStep(4); 
  // };


  return (
    <div>
      {step === 1 && <LoginForm onLoginSuccess={handleLoginSuccess} />}
    </div>

  );
};

export default LoginParent;