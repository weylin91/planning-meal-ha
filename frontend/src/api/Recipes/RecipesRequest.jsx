import axios from "axios";
import { useQuery } from "@tanstack/react-query";

/**
 * Custom hook to fetch ingredients with an optional filter.
 */
export const useIngredient = () => {
  return useQuery(["ingredients"], () => getIngredients());
};

export const getIngredients = async () => {
  const { data } = await axios.get("/api/meal_ha/foods");
  return data;
};
