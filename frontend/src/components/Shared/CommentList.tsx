import React, { useState, useEffect } from "react";
import { backendUrl } from "@/utils/utils";

interface Comment {
  comment_id: number;
  account_id: number;
  post_id: number;
  text: string;
  username: string;
  classifier: string;
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
          console.log(data);
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

  const sortedComments = comments.slice().sort((a, b) => {
    if (a.classifier === "POS" && b.classifier !== "POS") {
      return -1;
    }
    if (b.classifier === "POS" && a.classifier !== "POS") {
      return 1;
    }
    return 0;
  });

  const createAsterisks = (text: string) => "*".repeat(text.length);

  return (
    <div className="comment-list-container">
      {sortedComments.map((comment) => (
        <div key={comment.comment_id} className="comment">
          <div>
            <p className="text-red" style={{ fontSize: "80%" }}>
              {comment.username}
            </p>
            <p className="text-white">
              {comment.classifier && comment.classifier === "NEG"
                ? createAsterisks(comment.text)
                : comment.text}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CommentList;
