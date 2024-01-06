import Bottombar from "../Shared/Bottombar";
import Topbar from "../Shared/Topbar";
import React from "react";
import { Outlet } from "react-router-dom";

const RootLayout = () => {
  return (
    <div className="w-full flex flex-col min-h-screen">
      <Topbar />

      <section className="flex flex-1">
        <Outlet />
      </section>

      <Bottombar />
    </div>
  );
};

export default RootLayout;
