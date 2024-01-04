import React, { useState } from "react";
import abstractUser from "assets/icons/abstractUser.svg";

interface GridPostListProps {
  image: string;
  id: number;
  showUser?: boolean;
}

const GridPostList = ({ image, id, showUser = true }: GridPostListProps) => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const handleImageClick = (image: string) => {
    console.log(id);
    setSelectedImage(image);
  };

  const handleClose = () => {
    setSelectedImage(null);
  };

  return (
    <ul>
      <li className="relative min-w-80 h-80">
        <div className="grid-post_link">
          <img
            src={image}
            alt="post"
            className="h-full w-full object-cover"
            onClick={() => handleImageClick(image)}
          />
        </div>

        <div className="grid-post_user">
          {showUser && (
            <div className="flex items-center justify-start gap-2 flex-1">
              <img
                src={abstractUser}
                alt="creator"
                className="h-8 w-8 rounded-full"
              />
              <p className="line-clamp-1 text-gray-200">user Name</p>
            </div>
          )}
        </div>
      </li>
      {selectedImage && (
        <div className="overlay">
          <div className="overlay-inner">
            <div className="post-card ">
              <img src={selectedImage} alt="Selected" />
              <div className="post-content">
                {/* <h2>{postDescription}</h2> Titel des Beitrags */}
                <h2 className="text-white">Test Desctiption</h2>{" "}
                {/* Titel des Beitrags */}
              </div>
            </div>
            <div className="comments">
              <h3>Kommentare</h3>
              {/* {comments.map((comment, index) => (
                <div key={index} className="comment">
                  <p>
                    {comment.author}: {comment.text}
                  </p>
                </div>
              ))} */}
            </div>
            <button onClick={handleClose}>Schließen</button>
          </div>
        </div>
      )}
    </ul>
  );
};

export default GridPostList;
