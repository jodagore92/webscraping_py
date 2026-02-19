import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("../App.vue"), // De momento usamos App como landing
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../modules/auth/views/LoginView.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../modules/auth/views/RegisterView.vue"),
    },
    {
      path: "/search",
      name: "search",
      component: () => import("../modules/search/views/SearchView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/history",
      name: "history",
      component: () => import("../modules/search/views/HistoryView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/search/result/:id",
      name: "SearchDetails",
      component: () => import("../modules/search/views/SearchView.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next("/login");
  } else if (
    (to.name === "login" || to.name === "register") &&
    auth.isAuthenticated
  ) {
    next("/search");
  } else {
    next();
  }
});

export default router;
