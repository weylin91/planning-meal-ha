import path from "path";
import { URL } from "url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const __dirname = new URL(".", import.meta.url).pathname;

// https://vite.dev/config/
export default defineConfig({
	base: process.env.NODE_ENV === "production" ? "/local/meal_ha/" : "/",
	plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});

