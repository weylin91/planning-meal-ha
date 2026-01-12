import { Card, CardContent, TextField } from "@mui/material";
import "./App.css";

function App() {
	return (
		<>
			<Card sx={{ maxWidth: 345, margin: "auto", mt: 4 }}>
				<CardContent>
					<TextField label="Titre" variant="outlined" fullWidth />
				</CardContent>
			</Card>
		</>
	);
}

export default App;
