import loaderIcon from "assets/icons/loader.svg";

const Loader = () => (
  <div className="flex-center w-full">
    <img
      src={loaderIcon}
      alt="loader"
      width={24}
      height={24}
      className="animate-spin"
    />
  </div>
);

export default Loader;
