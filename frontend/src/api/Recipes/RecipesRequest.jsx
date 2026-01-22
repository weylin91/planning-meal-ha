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

const getApiUrl = () => {
  const envUrl = import.meta.env.VITE_APP_API_URL;
  if (envUrl && envUrl !== "") {
    return envUrl;
  }
  // Si en production (build local), fallback sur localhost
  return window.location.origin;
};

export const getIngredients = async () => {
  const { data } = await axios.get(`${getApiUrl()}/api/meal_ha/foods`, {
    withCredentials: true, // ← ENVOIE les cookies de session
    headers: {
      Authorization: `Bearer ${import.meta.env.VITE_APP_API_TOKEN}`,
    },
  });
  return data;
};

export const setNewIngredient = async (info) => {
  const { data } = await axios.post(`${getApiUrl()}/api/meal_ha/foods`, info, {
    withCredentials: true, // ← ENVOIE les cookies de session
    headers: {
      Authorization: `Bearer ${import.meta.env.VITE_APP_API_TOKEN}`,
    },
  });
  return data;
};
