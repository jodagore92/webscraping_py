<script setup>
import { computed } from 'vue';
import { useAuthStore } from './stores/auth';
import { Zap, ShoppingBag, History } from 'lucide-vue-next';

const auth = useAuthStore();

const destination = computed(() => auth.isAuthenticated ? '/search' : '/login');
</script>

<template>
  <router-view v-if="$route.path !== '/'" />

  <!-- Landing Page Simple -->
  <div v-else class="min-h-screen bg-linear-to-br from-green-50 to-white flex flex-col items-center justify-center p-4">
    <div class="max-w-4xl w-full text-center mt-12 md:mt-0">
      <div class="mb-8 flex justify-center">
        <div class="bg-white p-6 rounded-3xl shadow-2xl animate-bounce-slow">
          <span class="text-7xl">🕷️</span>
        </div>
      </div>
      <h1 class="text-6xl font-black text-gray-900 mb-6 tracking-tight">
        WebScraping <span class="text-green-600 italic">Pro</span>
      </h1>
      <p class="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed px-4">
        Compara precios en tiempo real de las mejores tiendas de Colombia.
        Ahorra tiempo y dinero con nuestra búsqueda inteligente unificada.
      </p>

      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <router-link :to="destination"
          class="bg-green-600 hover:bg-green-700 text-white px-10 py-4 rounded-2xl font-bold text-lg shadow-lg shadow-green-200 transition-all hover:-translate-y-1 hover:shadow-xl active:scale-95">
          {{ auth.isAuthenticated ? 'Ir al buscador' : 'Comenzar ahora' }}
        </router-link>
      </div>
    </div>

    <!-- Feature Cards -->
    <div class="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl w-full px-4">
      <router-link :to="destination"
        class="group bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-2xl hover:-translate-y-4 transition-all duration-300">
        <div
          class="bg-green-100 w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-green-500 transition-colors">
          <Zap class="text-green-600 group-hover:text-white transition-colors" :size="24" />
        </div>
        <div class="text-gray-900 mb-4 font-bold text-xl">Velocidad</div>
        <p class="text-gray-600 leading-relaxed text-sm">Búsquedas asíncronas optimizadas con Celery para resultados al
          instante.</p>
      </router-link>

      <router-link :to="destination"
        class="group bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-2xl hover:-translate-y-4 transition-all duration-300">
        <div
          class="bg-green-100 w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-green-500 transition-colors">
          <ShoppingBag class="text-green-600 group-hover:text-white transition-colors" :size="24" />
        </div>
        <div class="text-gray-900 mb-4 font-bold text-xl">Multi-Tienda</div>
        <p class="text-gray-600 leading-relaxed text-sm">Consultamos Éxito, Alkosto y más proveedores simultáneamente.
        </p>
      </router-link>

      <router-link :to="destination"
        class="group bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-2xl hover:-translate-y-4 transition-all duration-300">
        <div
          class="bg-green-100 w-12 h-12 rounded-xl flex items-center justify-center mb-6 group-hover:bg-green-500 transition-colors">
          <History class="text-green-600 group-hover:text-white transition-colors" :size="24" />
        </div>
        <div class="text-gray-900 mb-4 font-bold text-xl">Historial</div>
        <p class="text-gray-600 leading-relaxed text-sm">Guarda tus búsquedas favoritas y monitorea cambios en los
          precios.</p>
      </router-link>
    </div>
  </div>
</template>

<style>
/* Estilos globales via Tailwind */
.animate-bounce-slow {
  animation: bounce 3s infinite;
}

@keyframes bounce {

  0%,
  100% {
    transform: translateY(-5%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }

  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
</style>

<style>
/* Estilos globales via Tailwind */
</style>
