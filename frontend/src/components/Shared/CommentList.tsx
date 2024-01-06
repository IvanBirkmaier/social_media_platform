import React, { useState, useEffect } from "react";
import { backendUrl } from "@/utils/utils";

interface Comment {
  id: number;
  account_id: number;
  post_id: number;
  text: string;
  username: string;
}

interface CommentListProps {
  postId: number;
  updateTrigger: number;
}

const CommentList: React.FC<CommentListProps> = ({ postId, updateTrigger }) => {
  const [comments, setComments] = useState<Comment[]>([]);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`${backendUrl}/posts/${postId}/comments/`);
        if (response.ok) {
          const data = await response.json();
          setComments(data);
        } else {
          throw new Error("Fehler beim Laden der Kommentare");
        }
      } catch (error) {
        console.error("Fehler beim Abrufen der Kommentare von:", error);
      }
    };

    fetchComments();
  }, [postId, updateTrigger]);

  return (
    <div>
      {comments.map((comment) => (
        <div key={comment.id}>
          {/* Anpassen, wie Kommentare angezeigt werden sollen */}

          <div>
            <p className="text-red">{comment.username}</p>
            <p className="text-white">{comment.text}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CommentList;
