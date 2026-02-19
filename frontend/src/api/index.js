import api from "./axios";

export const authService = {
  async login(email, password) {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);
    const response = await api.post("/auth/login", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return response.data;
  },

  async register(userData) {
    const response = await api.post("/auth/register", userData);
    return response.data;
  },
};

export const searchService = {
  async search(query) {
    // El backend espera 'product' como query parameter en un POST.
    // Usamos params para la URL y eliminamos el body '{}' para evitar errores de validación.
    const response = await api.post("/search", null, {
      params: { product: query },
    });
    return response.data;
  },

  async getTaskStatus(taskId) {
    const response = await api.get(`/search/${taskId}`);
    return response.data;
  },
};

export const userService = {
  async getHistory(limit = 10, skip = 0) {
    const response = await api.get(
      `/users/me/history?limit=${limit}&skip=${skip}`,
    );
    return response.data;
  },
};
