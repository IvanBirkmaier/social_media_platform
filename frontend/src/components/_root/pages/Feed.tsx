import { useState, useEffect } from "react";
import Loader from "@/components/Shared/Loader";
import GridPostList from "@/components/Shared/GridPostList";
import searchLogo from "assets/icons/search.svg";
import { useAuth } from "@/components/Auth/AuthContext";
import { backendUrl } from "@/utils/utils";

interface Post {
  id: number;
  description: string;
  username: string;
  base64_image: string;
}

// Function to fetch random posts from FastAPI
const fetchRandomPosts = async (accountId: number) => {
  try {
    const response = await fetch(
      `${backendUrl}/posts/random/?account_id=${accountId}`
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    console.log(data.posts);
    return data.posts; // Adjusted to handle the new response structure
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
  }
};

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

const fetchAccountIdByUsername = async (username: string) => {
  try {
    const response = await fetch(`${backendUrl}/account-id/${username}`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data.account_id;
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
  }
};

// Beim Feed soll kein Post löschbar sein
const removePostFromList = () => {
  return;
};

const Feed = () => {
  const { user } = useAuth();
  const [posts, setPosts] = useState<Post[]>([]);
  const [searchedPosts, setSearchedPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchValue, setSearchValue] = useState("");
  const [searched_accountId, setAccountId] = useState(null);

  useEffect(() => {
    const loadPosts = async () => {
      const accountId = user?.id || 0;
      const fetchedPosts = await fetchRandomPosts(accountId);
      if (fetchedPosts) {
        setPosts(fetchedPosts);
        setIsLoading(false);
      }
    };

    loadPosts();
  }, []);

  useEffect(() => {
    setSearchedPosts([]);

    if (searchValue && searchValue != user?.username) {
      fetchAccountIdByUsername(searchValue)
        .then((id) => {
          setAccountId(id);
        })
        .catch((error) => {
          console.error("Error fetching account ID:", error);
          setAccountId(null);
        });
    }
  }, [searchValue]);

  useEffect(() => {
    const loadSearchedPosts = async () => {
      if (searched_accountId !== null && searched_accountId !== 0) {
        setIsLoading(true);
        const posts = await fetchAccountPosts(searched_accountId);
        if (posts) {
          setSearchedPosts(posts);
        }
        setIsLoading(false);
      }
    };

    loadSearchedPosts();
  }, [searched_accountId]);

  const shouldShowSearchResults = searchValue !== "";

  const formatBase64Image = (base64String: string) => {
    if (!base64String) {
      return "";
    }

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
      <div className="explore-inner_container">
        <div className="flex gap-1 px-4 w-full rounded-lg bg-gray-300">
          <img src={searchLogo} width={24} height={24} alt="search" />
          <input
            type="text"
            placeholder="Search"
            className="explore-search"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
          />
        </div>
      </div>

      <div className="flex-between w-full max-w-5xl mt-16 mb-7">
        <h2 className="h3-bold md:h2-bold w-full">Feed of {user?.username}</h2>
        {/* ...other elements */}
      </div>

      <div className="grid-container">
        {isLoading ? (
          <Loader />
        ) : shouldShowSearchResults ? (
          searchedPosts.length > 0 ? (
            searchedPosts.map((post, index) => (
              <GridPostList
                image={formatBase64Image(post.base64_image)}
                description={post.description}
                id={post.id}
                showUser={user?.username !== post.username}
                username={post.username}
                key={index}
                removePost={removePostFromList}
              />
            ))
          ) : (
            <p className="text-light-4 mt-10 text-center w-full">
              No posts found
            </p>
          )
        ) : posts.length === 0 ? (
          <p className="text-light-4 mt-10 text-center w-full">
            No posts found
          </p>
        ) : (
          posts.map((post, index) => (
            <GridPostList
              image={formatBase64Image(post.base64_image)}
              description={post.description}
              id={post.id}
              showUser={true}
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

export default Feed;
