import { useFormik } from "formik";
import { useEffect, useState } from "react";
import { DeleteForever, List, Settings } from "@mui/icons-material";
import {
  Box,
  Button,
  Chip,
  Divider,
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import {
  Autocomplete,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  Paper,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import { amber } from "@mui/material/colors";
import { useQueryClient } from "@tanstack/react-query";
import {
  setNewIngredient,
  useIngredient,
} from "../../api/Recipes/RecipesRequest.jsx";

const ListRecipes = () => {
  const [openNewRecipe, setOpenNewRecipe] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [recipes, setRecipes] = useState({
    recipes: [
      {
        id: 1,
        title: "Spaghetti Bolognese",
        type: "Plat principal",
        products: [
          { id: 1, name: "Spaghetti" },
          { id: 2, name: "Viande hachée" },
          { id: 3, name: "Sauce tomate" },
        ],
      },
      {
        id: 2,
        title: "Salade César",
        type: "Entrée",
        products: [
          { id: 4, name: "Laitue" },
          { id: 5, name: "Poulet grillé" },
          { id: 6, name: "Parmesan" },
        ],
      },
    ],
  });

  return (
    <Box>
      <Box sx={{ display: "flex", justifyContent: "space-between", p: 3 }}>
        <Button variant="outlined" onClick={() => setOpenNewRecipe(true)}>
          Ajouter une recette
        </Button>
      </Box>
      <TableContainer fullWidth>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>
                <Box display="flex" alignItems="center">
                  Nom
                </Box>
              </TableCell>
              <TableCell>
                <Box display="flex" alignItems="center">
                  Type
                </Box>
              </TableCell>
              <TableCell>Ingrédients</TableCell>
              <TableCell align="right">Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {recipes.recipes.length > 0 &&
              recipes.recipes.map((recipe) => (
                <RecetteItem recipe={recipe} key={recipe.id}></RecetteItem>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <AddRecipe
        openNewRecipe={openNewRecipe}
        setOpenNewRecipe={setOpenNewRecipe}
        selectedRecipe={selectedRecipe}
        setSelectedRecipe={setSelectedRecipe}
      />
    </Box>
  );
};

const RecetteItem = ({ recipe }) => {
  const [hover, setHover] = useState(false);
  const [menuState, setMenuState] = useState({ anchorEl: null, listId: null });
  const openMenu = Boolean(menuState.anchorEl);

  const handleClick = (event, listId) => {
    setMenuState({ anchorEl: event.currentTarget, listId });
  };
  const handleClose = () => {
    setMenuState({ anchorEl: null, listId: null });
  };
  return (
    <TableRow
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      sx={{
        cursor: "pointer",
        backgroundColor: hover ? amber[800] : "transparent",
      }}
    >
      <TableCell>{recipe.title}</TableCell>
      <TableCell>{recipe.type}</TableCell>
      <TableCell>
        {recipe.products.map((product) => (
          <Chip
            sx={{ mr: 1, mb: 1, mt: 1 }}
            key={product.id}
            label={product.name}
            size="small"
          />
        ))}
      </TableCell>
      <TableCell align="right">
        <IconButton onClick={(e) => handleClick(e, recipe.id)}>
          <List />
        </IconButton>
        <Menu
          anchorEl={menuState.anchorEl}
          open={openMenu}
          onClose={handleClose}
        >
          <MenuItem>
            <ListItemIcon>
              <Settings fontSize="small" />
            </ListItemIcon>
            <ListItemText>Modifier</ListItemText>
          </MenuItem>
          <Divider />
          <MenuItem>
            <ListItemIcon>
              <DeleteForever fontSize="small" />
            </ListItemIcon>
            <ListItemText>Supprimer</ListItemText>
          </MenuItem>
        </Menu>
      </TableCell>
    </TableRow>
  );
};

const AddRecipe = ({
  openNewRecipe,
  setOpenNewRecipe,
  selectedRecipe,
  setSelectedRecipe,
}) => {
  const { data: ingredients, isLoading } = useIngredient();
  const isDev = process.env.NODE_ENV === "development";
  const mockIngredients = {
    foods: [{ id: 1, name: "Filet de poulet" }],
  };
  //const { mutate: newRecipe } = useNewRecipe();
  //const { mutate: updateRecipe } = useUpdateRecipe(); // <-- crée ce hook si besoin

  const queryClient = useQueryClient();

  const [saisie, setSaisie] = useState("");

  const formik = useFormik({
    initialValues: {
      title: "",
      category: "",
      nbMeals: 1,
      type: "dish",
      products: [],
    },
    onSubmit: (values) => {
      const dataToSend = {
        ...values,
        products: values.products.map((p) => p.id), // <-- transforme en tableau d'IDs
      };
    },
  });

  useEffect(() => {
    if (selectedRecipe) {
      formik.setValues({
        title: selectedRecipe.title,
        category: selectedRecipe.category,
        nbMeals: selectedRecipe.nbMeals ?? 1,
        type: selectedRecipe.type ?? "main",
        products: selectedRecipe.products,
      });
    } else {
      formik.resetForm();
    }
  }, [selectedRecipe]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const ingredientsData = isDev ? mockIngredients : ingredients;
  console.log("INGREDIENTS :", ingredientsData);

  return (
    <Dialog open={openNewRecipe} maxWidth="md" fullWidth={true}>
      <DialogTitle>Ajouter une recette</DialogTitle>
      <DialogContent>
        <form onSubmit={formik.handleSubmit} id="recipeForm">
          <Grid container spacing={2} paddingTop={2}>
            <Grid size={{ xs: 12, mb: 2 }}>
              <Typography
                variant="body2"
                sx={{ mb: 1, textTransform: "uppercase" }}
              >
                Nom :
              </Typography>
              <TextField
                size="small"
                fullWidth
                value={formik.values.title}
                onChange={(e) => formik.setFieldValue("title", e.target.value)}
                onBlur={formik.handleBlur}
              />
            </Grid>
            <Grid size={{ xs: 4, mb: 2 }}>
              <Typography
                variant="body2"
                sx={{ mb: 1, textTransform: "uppercase" }}
              >
                Catégorie :
              </Typography>
              <Select
                value={formik.values.category}
                onChange={(e) =>
                  formik.setFieldValue("category", e.target.value)
                }
                onBlur={formik.handleBlur}
                fullWidth
                size="small"
              >
                <MenuItem value="Viande">Viande</MenuItem>
                <MenuItem value="Poisson">Poisson</MenuItem>
                <MenuItem value="Végan">Végan</MenuItem>
                <MenuItem value="Léger">Léger</MenuItem>
                <MenuItem value="Fast food">Fast food</MenuItem>
              </Select>
            </Grid>
            <Grid size={{ xs: 4, mb: 2 }}>
              <Typography
                variant="body2"
                sx={{ mb: 1, textTransform: "uppercase" }}
              >
                Catégorie :
              </Typography>
              <Select
                value={formik.values.category}
                onChange={(e) =>
                  formik.setFieldValue("category", e.target.value)
                }
                onBlur={formik.handleBlur}
                fullWidth
                size="small"
              >
                <MenuItem value="dish">Plât</MenuItem>
                <MenuItem value="side">Accompagnement</MenuItem>
              </Select>
            </Grid>
            <Grid size={{ xs: 4, mb: 2 }}>
              <Typography
                variant="body2"
                sx={{ mb: 1, textTransform: "uppercase" }}
              >
                Nombre de repas :
              </Typography>
              <TextField
                size="small"
                type="number"
                fullWidth
                value={formik.values.nbMeals}
                onChange={(e) =>
                  formik.setFieldValue("nbMeals", e.target.value)
                }
                onBlur={formik.handleBlur}
                inputProps={{
                  style: { MozAppearance: "textfield" },
                  inputMode: "numeric",
                  pattern: "[0-9]*",
                  min: 1,
                  // Hide spin buttons for Chrome, Safari, Edge, Opera
                  sx: {
                    "&::-webkit-outer-spin-button, &::-webkit-inner-spin-button":
                      {
                        WebkitAppearance: "none",
                        margin: 0,
                      },
                  },
                }}
                sx={{
                  // Hide spin buttons for Chrome, Safari, Edge, Opera
                  "& input[type=number]::-webkit-outer-spin-button, & input[type=number]::-webkit-inner-spin-button":
                    {
                      WebkitAppearance: "none",
                      margin: 0,
                    },
                  // Hide spin buttons for Firefox
                  "& input[type=number]": {
                    MozAppearance: "textfield",
                  },
                }}
              />
            </Grid>
            <Grid size={{ xs: 12, mb: 2 }}>
              <Typography
                variant="body2"
                sx={{ mb: 1, textTransform: "uppercase" }}
              >
                Ingrédients :
              </Typography>
              <Autocomplete
                multiple
                options={ingredientsData?.foods}
                getOptionLabel={(option) => option.name}
                getOptionKey={(option) => option.id}
                size="small"
                value={
                  Array.isArray(formik.values.products)
                    ? formik.values.products
                    : []
                }
                onChange={(_, value) => formik.setFieldValue("products", value)}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    onKeyUp={(e) => setSaisie(e.target.value)}
                  />
                )}
                PaperComponent={({ children }) => (
                  <Paper sx={{ maxHeight: 300, overflow: "auto" }}>
                    <Button
                      color="primary"
                      fullWidth
                      sx={{ justifyContent: "flex-start", pl: 2 }}
                      onMouseDown={async (e) => {
                        e.preventDefault();
                        await setNewIngredient({
                          name: saisie,
                          category: "ingredient",
                        }).then(() => {
                          queryClient.invalidateQueries(["ingredients"]);
                        });
                        setSaisie("");
                      }}
                    >
                      + Ajouter cet ingrédient
                    </Button>
                    {children}
                  </Paper>
                )}
                fullWidth
              />
            </Grid>
          </Grid>
        </form>
      </DialogContent>
      <DialogActions>
        <Button
          onClick={() => {
            setOpenNewRecipe(false);
            setSelectedRecipe(null);
            formik.resetForm();
          }}
        >
          Annuler
        </Button>
        <Button type="submit" form="recipeForm">
          Enregistrer
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ListRecipes;
