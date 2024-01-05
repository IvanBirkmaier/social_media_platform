import React, { useState } from "react";
import abstractUser from "assets/icons/abstractUser.svg";

interface GridPostListProps {
  image: string; // Base64 encoded image string
  description: string;
  id: number;
  showUser?: boolean;
}

const IMAGE_RESOLUTION = { width: 800, height: 450 }; // Beispielauflösung

const GridPostList = ({
  image,
  id,
  showUser = true,
  description,
}: GridPostListProps) => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const handleImageClick = (image: string) => {
    console.log(id);
    setSelectedImage(image);
  };

  const handleClose = () => {
    setSelectedImage(null);
  };

  // Ensure the base64 string is formatted for HTML image source
  const formattedImage = image.startsWith("data:image/jpeg;base64,")
    ? image
    : `data:image/jpeg;base64,${image}`;

  return (
    <ul>
      <li className="relative min-w-80 h-80">
        <div className="grid-post_link">
          <img
            src={formattedImage}
            alt="post"
            className="h-full w-full object-cover object-center"
            onClick={() => handleImageClick(image)}
          />
        </div>

        {showUser && (
          <div className="grid-post_user">
            <div className="flex items-center justify-start gap-2 flex-1">
              <img
                src={abstractUser}
                alt="creator"
                className="h-8 w-8 rounded-full"
              />
              <p className="line-clamp-1 text-gray-200">User Name</p>
            </div>
          </div>
        )}
      </li>

      {selectedImage && (
        <div className="overlay">
          {/* <div className="overlay-inner"> */}
          <div className="post_details-card">
            <img
              src={selectedImage}
              className="post_details-img" // h-full w-full object-cover object-center Verwende object-fit und object-position
              style={{
                width: IMAGE_RESOLUTION.width,
                height: IMAGE_RESOLUTION.height,
              }} // Setze die Auflösung für alle Bilder
              alt="Selected"
            />
            <div className="post_details-info">
              <h3 className="text-white">{description}</h3>
              {/* <div className="post_details-info"> */}
              <hr className="parting_line" />
              <input type="text" />
            </div>

            {/* Comment section can be implemented here */}
            {/* </div> */}
          </div>
          <button onClick={handleClose} className="text-red">
            Close
          </button>
          {/* </div> */}
        </div>
      )}
    </ul>
  );
};

export default GridPostList;
