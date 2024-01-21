import React, { useState, useEffect } from "react";
import { websocketServerUrl, url_microservice_three } from "@/utils/utils";

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
}

const CommentList: React.FC<CommentListProps> = ({ postId }) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  // Funktion zum Abrufen von Kommentaren
  const fetchComments = async () => {
    try {
      const response = await fetch(`${url_microservice_three}/posts/${postId}/comments/`);
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

  // WebSocket-Verbindung aufbauen
  useEffect(() => {
    console.log(websocketServerUrl)
    const websocket = new WebSocket(`${websocketServerUrl}`);
    websocket.onopen = () => console.log("Connected to WS Server");
    websocket.onmessage = (event) => {
      // event.data enthält die vom Server gesendete Nachricht
      console.log("Nachricht vom Server erhalten:", event.data);
    
      // Kommentare neu laden
      fetchComments();
    };

    websocket.onclose = () => console.log("Disconnected from WS Server");

    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, [postId]);

  useEffect(() => {
    if (ws) {
      console.log("WebSocket-Status:", ws.readyState);
    }
  }, [ws]);

  // Kommentare beim ersten Laden und bei Änderungen von postId abrufen
  useEffect(() => {
    fetchComments();
  }, [postId]);

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
