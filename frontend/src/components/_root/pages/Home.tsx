import React, { useState } from "react";
import photo from "assets/examplePost.jpeg";
import photo1 from "assets/post2.jpeg";
import photo2 from "assets/post3.jpg";
import searchLogo from "assets/icons/search.svg";
import Loader from "@/components/Shared/Loader";
import GridPostList from "@/components/Shared/GridPostList";

const Home = () => {
  const images = [
    photo,
    photo1,
    photo2,
    photo2,
    photo,
    photo1,
    photo1,
    photo2,
    photo,
  ];

  // get_random_posts_not_by_account
  // const posts = [];

  // if (!posts) {
  //   return (
  //     <div className="flex-center w-full h-full">
  //       <Loader></Loader>
  //     </div>
  //   );
  // }

  const [searchValue, setSearchValue] = useState("");

  const shouldShowSearchResults = searchValue !== "";
  // const shouldShowPosts =
  //   !shouldShowSearchResults &&
  //   posts.pages.every((item) => item.documents.length === 0);
  const shouldShowPosts = !shouldShowSearchResults && images.length === 0;

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
            onChange={(e) => {
              const { value } = e.target;
              setSearchValue(value);
            }}
          />
        </div>
      </div>

      <div className="flex-between w-full max-w-5xl mt-16 mb-7">
        <h2 className="h3-bold md:h2-bold w-full">Home</h2>
        <div className="flex-center gap-3 bg-gray-300 rounded-xl px-4 py-2 cusror-pointer">
          <p className="small-medium md:base-medium text-light-4">Filter</p>
        </div>
      </div>

      {/* <div className="flex flex-wrap gap-9 w-full max-w-5xl"> */}
      <div className="grid-container">
        {shouldShowSearchResults ? (
          <p>Show Search Results</p>
        ) : shouldShowPosts ? (
          <p className="text-light-4 mt-10 text-center w-full">End of posts</p>
        ) : (
          images.map((item, index) => (
            // <GridPostList key={'page-${index}' posts = {item.documents}}
            <GridPostList image={item} id={index} showUser={true} key={index} />
          ))
        )}
      </div>
    </div>
  );
};

export default Home;
