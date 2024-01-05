import React from "react";
import { Button } from "../ui/button";
import { useNavigate } from "react-router-dom";
import addPost from "assets/icons/addPost.png";

const Bottombar = () => {
  const navigate = useNavigate();

  return (
    <section className="bottom-bar">
      <div className="flex-between py-4 px-5 h-5">
        <Button variant="ghost" className="shad-button_ghost">
          <img
            src={addPost}
            alt="addPost"
            className="h-10 w-auto"
            onClick={() => navigate("/addPost")}
          ></img>
          <p className="text-3xl">Add Post</p>
        </Button>
      </div>
    </section>
  );
};

export default Bottombar;
