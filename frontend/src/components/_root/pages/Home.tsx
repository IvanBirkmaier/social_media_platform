import { useState, useEffect } from "react";
import Loader from "@/components/Shared/Loader";
import GridPostList from "@/components/Shared/GridPostList";
import { useAuth } from "@/components/Auth/AuthContext";
import { backendUrl } from "@/utils/utils";

interface Post {
  id: number;
  description: string;
  username: string;
  base64_image: string;
}

const fetchAccountPosts = async (accountId: number) => {
  try {
    const response = await fetch(`${backendUrl}/account/${accountId}/posts`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data.posts; // Adjusted to handle the new response structure
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
  }
};

const Home = () => {
  const { user } = useAuth();
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadPosts = async () => {
      const accountId = user?.id || 0;
      const fetchedPosts = await fetchAccountPosts(accountId);
      if (fetchedPosts) {
        setPosts(fetchedPosts);
        setIsLoading(false);
      }
    };

    loadPosts();
  }, [user?.id]);

  // zum aktualisieren der Post Liste
  const removePostFromList = (postId: number) => {
    setPosts((prevPosts) => prevPosts.filter((post) => post.id !== postId));
  };

  const formatBase64Image = (base64String: string) => {
    // Prüfen, ob der String bereits mit dem korrekten Präfix beginnt
    if (base64String.startsWith("data:image/jpeg;base64,")) {
      return base64String;
    } else {
      // Ersetzen eines fehlerhaften Präfixes, falls vorhanden
      const correctedString = base64String.replace(
        "dataimage/jpegbase64",
        "data:image/jpeg;base64,"
      );
      // Überprüfen, ob der String überhaupt ein Präfix hat
      if (correctedString.startsWith("data:")) {
        return correctedString;
      } else {
        // Korrektes Präfix hinzufügen, falls es ganz fehlt
        return `data:image/jpeg;base64,${correctedString}`;
      }
    }
  };

  return (
    <div className="explore-container">
      <div className="flex-between w-full max-w-5xl mt-5 mb-7">
        <h2 className="h3-bold md:h2-bold w-full">Home of {user?.username}</h2>
        {/* ...other elements */}
      </div>

      <div className="grid-container">
        {isLoading ? (
          <Loader />
        ) : posts.length === 0 ? (
          <p className="text-light-4 mt-10 text-center w-full">
            No posts found, create one
          </p>
        ) : (
          posts.map((post, index) => (
            <GridPostList
              image={formatBase64Image(post.base64_image)}
              description={post.description}
              id={post.id}
              showUser={false}
              username={post.username}
              key={index}
              removePost={removePostFromList}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Home;
