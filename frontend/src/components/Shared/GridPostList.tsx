import React, { useState, useEffect, useRef } from "react";
import abstractUser from "assets/icons/abstractUser.svg";
import { useAuth } from "../Auth/AuthContext";
import { backendUrl } from "@/utils/utils";
import CommentList from "./CommentList";
import post_svg from "assets/icons/arrow_right.svg";
import deleteIcon from "assets/icons/delete.svg";

interface GridPostListProps {
  image: string; // Base64 encoded image string
  description: string;
  id: number;
  showUser?: boolean;
  username: string;
  removePost: (postId: number) => void;
}

const IMAGE_RESOLUTION = { width: 1000, height: 562 }; // Beispielauflösung

const GridPostList = ({
  image,
  id,
  showUser = true,
  description,
  username,
  removePost,
}: GridPostListProps) => {
  const { user } = useAuth();
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const [comment, setComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [commentsUpdateTrigger, setCommentsUpdateTrigger] = useState(0); // Neuer Zustand
  const [fullImage, setFullImage] = useState<string | null>(null); // Zustand für das vollständige Bild

  const fetchFullImage = async (postId: number) => {
    try {
      const response = await fetch(`${backendUrl}/posts/${postId}/image/`, {
        method: "GET",
      });
      if (response.ok) {
        const data = await response.json();
        setFullImage(data.full_image); // Setzen des vollen Bildes
      } else {
        throw new Error("Fehler beim Laden des vollen Bildes");
      }
    } catch (error) {
      console.error("Fehler beim Laden des vollen Bildes", error);
    }
  };

  const handleImageClick = (image: string) => {
    console.log(id);
    setSelectedImage(image);
    fetchFullImage(id);
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this post?")) {
      try {
        const response = await fetch(`${backendUrl}/posts/${id}/`, {
          method: "DELETE",
        });

        if (!response.ok) {
          throw new Error("Fehler beim Löschen des Beitrags");
        }

        removePost(id);
        setFullImage(null);
        // Hier können Sie zusätzliche Logik hinzufügen, z.B. das Entfernen des Beitrags aus dem State
      } catch (error) {
        console.error("Fehler beim Löschen des Beitrags", error);
      }
    }
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
      const response = await fetch(`${backendUrl}/comments/`, {
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
        setCommentsUpdateTrigger((prev) => prev + 1); // Aktualisieren des Triggers
      } else {
        throw new Error("Fehler beim Senden des Kommentars");
      }
    } catch (error) {
      console.error("Fehler beim Senden des Kommentars", error);
    }
    setIsSubmitting(false);
  };

  return (
    <ul>
      <li className="relative min-w-80 h-80">
        <div className="grid-post_link">
          <img
            src={image}
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
              src={fullImage || selectedImage} // fullImage wird verwendet, wenn es vorhanden ist
              loading="lazy"
              role="presentation"
              className="post_details-img" // h-full w-full object-cover object-center Verwende object-fit und object-position
              style={{
                width: IMAGE_RESOLUTION.width,
                height: IMAGE_RESOLUTION.height,
              }} // Setze die Auflösung für alle Bilder
              decoding="async"
              alt="Selected"
            />
            <div className="post_details-info">
              <div className="w-full flex items-center justify-between">
                <h3 className="text-orange-300 h3-bold">{username}</h3>
                {!showUser && (
                  <img
                    src={deleteIcon}
                    alt="Löschen"
                    className="cursor-pointer h-6 w-auto" // Cursor-Style für Klickbarkeit
                    onClick={handleDelete}
                  />
                )}
              </div>

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

              <div className="comment_input_container">
                <input
                  className="comment_input"
                  type="text"
                  placeholder="Kommentiere"
                  value={comment}
                  onChange={handleCommentChange}
                />
                <img
                  src={post_svg}
                  alt="Posten"
                  onClick={isSubmitting ? () => {} : submitComment}
                  style={{
                    cursor: isSubmitting ? "not-allowed" : "pointer", // Zeige Handzeiger bei Hover
                    width: "29px",
                    height: "29px",
                  }}
                />
              </div>

              <CommentList postId={id} updateTrigger={commentsUpdateTrigger} />
            </div>
          </div>
        </div>
      )}
    </ul>
  );
};

export default GridPostList;
