import axios from "axios";
import { useQuery } from "@tanstack/react-query";

/**
 * Custom hook to fetch ingredients with an optional filter.
 */
export const useIngredient = () => {
  return useQuery({
    queryKey: ["ingredients"],
    queryFn: getIngredients,
    select: (data) => (Array.isArray(data) ? data : data.foods || []),
  });
};

export const getIngredients = async () => {
  const { data } = await axios.get("/api/meal_ha/foods", {
    withCredentials: true, // ← ENVOIE les cookies de session
  });
  return data;
};

export const setNewIngredient = async (info) => {
  const { data } = await axios.post("/api/meal_ha/foods", info, {
    withCredentials: true, // ← ENVOIE les cookies de session
  });
  return data;
};
