import { Card ,Grid } from "@mui/material";
import "./App.css";
import ListRecipes from "./components/ListRecipes";

function App() {
	return (
    <>
      <Grid container fullWidth spacing={2} padding={2} >
        <Grid size={{xs:12}}>
            <Card>
              <ListRecipes />
            </Card>
        </Grid>
      </Grid>
    </>
	);
}

export default App;
