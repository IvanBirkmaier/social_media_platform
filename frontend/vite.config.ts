import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import { resolve } from "path";
import path from "path";

export default defineConfig({
  base: "/",
  plugins: [react()],
  resolve: {
    alias: {
      components: resolve(__dirname, "src/components"),
      assets: resolve(__dirname, "src/assets"),
      constants: resolve(__dirname, "src/constants"),
      views: resolve(__dirname, "src/views"),
      utils: resolve(__dirname, "src/utils"),
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    sourcemap: true,
    minify: false,
  },
});
