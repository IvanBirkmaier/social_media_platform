import Bottombar from "../Shared/Bottombar";
import LeftSidebar from "../Shared/LeftSidebar";
import Topbar from "../Shared/Topbar";
import React from "react";
import { Outlet } from "react-router-dom";

const RootLayout = () => {
  return (
    <div className="w-full">
      <Topbar />
      {/* <LeftSidebar /> */}

      <section className="flex flex-1 h-full">
        <Outlet />
      </section>

      <Bottombar />
    </div>
  );
};

export default RootLayout;
