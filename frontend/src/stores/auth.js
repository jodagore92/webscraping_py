import { defineStore } from "pinia";
import { authService } from "../api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")) || null,
    token: localStorage.getItem("token") || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      this.loading = true;
      this.error = null;
      try {
        const data = await authService.login(email, password);
        this.token = data.access_token;
        // El backend actual solo devuelve el token, pondremos un placeholder o fetch user luego
        this.user = { email };
        localStorage.setItem("token", this.token);
        localStorage.setItem("user", JSON.stringify(this.user));
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || "Error al iniciar sesión";
        return false;
      } finally {
        this.loading = false;
      }
    },

    async register(userData) {
      this.loading = true;
      this.error = null;
      try {
        await authService.register(userData);
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || "Error al registrarse";
        return false;
      } finally {
        this.loading = false;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
  },
});
