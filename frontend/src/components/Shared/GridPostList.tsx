import React, { useState, useEffect, useRef } from "react";
import abstractUser from "assets/icons/abstractUser.svg";
import { useAuth } from "../Auth/AuthContext";

interface GridPostListProps {
  image: string; // Base64 encoded image string
  description: string;
  id: number;
  showUser?: boolean;
  username: string;
}

const IMAGE_RESOLUTION = { width: 1000, height: 562 }; // Beispielauflösung

const GridPostList = ({
  image,
  id,
  showUser = true,
  description,
  username,
}: GridPostListProps) => {
  const { user } = useAuth();
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const [comment, setComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleImageClick = (image: string) => {
    console.log(id);
    setSelectedImage(image);
  };

  // close overlay if click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        overlayRef.current &&
        !overlayRef.current.contains(event.target as Node)
      ) {
        setSelectedImage(null);
      }
    };

    if (selectedImage) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [selectedImage]);

  // Comment
  const handleCommentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setComment(e.target.value);
  };

  const submitComment = async () => {
    if (comment.trim() === "") return; // Prüfen, ob der Kommentar leer ist

    setIsSubmitting(true);
    try {
      const response = await fetch("http://localhost:8000/comments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Fügen Sie weitere Header hinzu, falls erforderlich (z.B. für die Authentifizierung)
        },
        body: JSON.stringify({
          account_id: user?.id,
          post_id: id,
          text: comment,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setComment(""); // Kommentarfeld zurücksetzen
      } else {
        throw new Error("Fehler beim Senden des Kommentars");
      }
    } catch (error) {
      console.error("Fehler beim Senden des Kommentars", error);
    }
    setIsSubmitting(false);
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
              <p className="line-clamp-1 text-gray-200">{username}</p>
            </div>
          </div>
        )}
      </li>

      {selectedImage && (
        <div className="overlay">
          {/* <div className="overlay-inner"> */}
          <div ref={overlayRef} className="post_details-card">
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
              <h3 className="text-orange-300 h3-bold">{username}</h3>
              <h2
                className="text-white"
                style={{
                  wordWrap: "break-word",
                  overflowWrap: "break-word",
                  wordBreak: "break-all",
                  whiteSpace: "normal",
                }}
              >
                {description}
              </h2>

              <hr className="parting_line" />
              <input
                className="comment_input"
                type="text"
                placeholder="Kommentiere"
                value={comment}
                onChange={handleCommentChange}
              />
              <button
                className="submit_comment_button text-lime-300"
                onClick={submitComment}
                disabled={isSubmitting}
              >
                Posten
              </button>
            </div>
          </div>
        </div>
      )}
    </ul>
  );
};

export default GridPostList;
