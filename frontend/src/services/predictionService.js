import api from "../api/api";

export const getPredictions = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/prediction/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};