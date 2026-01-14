import { amber } from "@mui/material/colors";
import { createTheme } from "@mui/material/styles";

const DarkTheme = createTheme({
  palette: {
    mode: "dark",
    background: {
      default: "#303339",
    },
    primary: {
      main: amber[400],
    },
  },
});

export default DarkTheme;
