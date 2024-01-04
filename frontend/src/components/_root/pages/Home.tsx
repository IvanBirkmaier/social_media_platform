import React, { useState, useEffect } from "react";
import Loader from "@/components/Shared/Loader";
import GridPostList from "@/components/Shared/GridPostList";
import searchLogo from "assets/icons/search.svg";

// Function to fetch random posts from FastAPI
// const fetchRandomPosts = async (accountId: number) => {
//   try {
//     const response = await fetch(
//       `http://localhost:8000/posts/random/?account_id=${accountId}`
//     );
//     if (!response.ok) {
//       throw new Error("Network response was not ok");
//     }
//     return await response.json();
//   } catch (error) {
//     console.error("There has been a problem with your fetch operation:", error);
//   }
// };

const fetchRandomPosts = async (accountId: number) => {
  try {
    const response = await fetch(
      `http://localhost:8000/posts/random/?account_id=${accountId}`
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
    const response = await fetch(
      `http://localhost:8000/account/${accountId}/posts`
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data.posts; // Adjusted to handle the new response structure
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
  }
};

// const fetchAccountPosts = async (accountId: number) => {
//   try {
//     const response = await fetch(
//       `http://localhost:8000/account/${accountId}/posts`
//     );
//     if (!response.ok) {
//       throw new Error("Network response was not ok");
//     }
//     return await response.json();
//   } catch (error) {
//     console.error("There has been a problem with your fetch operation:", error);
//   }
// };

const Home = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchValue, setSearchValue] = useState("");

  useEffect(() => {
    const loadPosts = async () => {
      const accountId = 2; // Replace with the actual account ID as needed
      const fetchedPosts = await fetchRandomPosts(accountId);
      if (fetchedPosts) {
        setPosts(fetchedPosts);
        setIsLoading(false);
      }
    };

    loadPosts();
  }, []);

  const shouldShowSearchResults = searchValue !== "";

  const formatBase64Image = (base64String) => {
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
        <h2 className="h3-bold md:h2-bold w-full">Home</h2>
        {/* ...other elements */}
      </div>

      <div className="grid-container">
        {isLoading ? (
          <Loader />
        ) : shouldShowSearchResults ? (
          <p>Show Search Results</p>
        ) : posts.length === 0 ? (
          <p className="text-light-4 mt-10 text-center w-full">
            No posts found
          </p>
        ) : (
          posts.map((post: any, index) => (
            <GridPostList
              image={formatBase64Image(post.base64_image)} // Stellt sicher, dass das Präfix korrekt ist// Assuming the image is in JPEG format
              id={post.id}
              showUser={true}
              key={index}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Home;
