import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import queryClient from "@/utils/react-query";
import "@fontsource/roboto";
// Specify weight
import "@fontsource/roboto/400-italic.css";
// Defaults to weight 400
import "@fontsource/roboto/400.css";
import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import { StyledEngineProvider } from "@mui/material/styles";
import { QueryClientProvider } from "@tanstack/react-query";
import App from "./App.jsx";
import darkTheme from "./utils/DarkTheme.jsx";

// Specify weight and style

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={darkTheme}>
        <QueryClientProvider client={queryClient}>
          <CssBaseline />
          <App />
        </QueryClientProvider>
      </ThemeProvider>
    </StyledEngineProvider>
  </StrictMode>,
);
