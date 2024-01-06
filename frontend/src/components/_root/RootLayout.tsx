import Bottombar from "../Shared/Bottombar";
import LeftSidebar from "../Shared/LeftSidebar";
import Topbar from "../Shared/Topbar";
import React from "react";
import { Outlet } from "react-router-dom";

const RootLayout = () => {
  return (
    <div className="w-full flex flex-col min-h-screen">
      <Topbar />
      {/* <LeftSidebar /> */}

      <section className="flex flex-1">
        <Outlet />
      </section>

      <Bottombar />
    </div>
  );
};

export default RootLayout;
