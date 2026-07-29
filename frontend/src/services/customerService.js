import api from "../api/api";

export const getCustomers = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/customers/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};