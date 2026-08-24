import api from "../api/api";

export const getLoans = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/loans/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const deleteLoan = async (loanId) => {
  const token = localStorage.getItem("token");

  return api.delete(`/loans/${loanId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const updateLoanStatus = async (loanId, status) => {
  const token = localStorage.getItem("token");

  return api.put(
    `/loans/${loanId}/status`,
    { status },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
};