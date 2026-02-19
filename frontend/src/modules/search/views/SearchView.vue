<script setup>
import { ref, onUnmounted, computed, onMounted, watch } from 'vue';
import { searchService, userService } from '../../../api';
import { useAuthStore } from '../../../stores/auth';
import { useSearchStore } from '../../../stores/search';
import { useRouter, useRoute } from 'vue-router';
import { Search, Loader2, ExternalLink, History as HistoryIcon, LogOut, Filter, ArrowUpDown } from 'lucide-vue-next';

const auth = useAuthStore();
const searchStore = useSearchStore();
const router = useRouter();
const route = useRoute();
const query = ref('');
const taskId = ref(null);
const results = ref([]);
const status = ref('idle'); // idle, searching, completed, error
const intervalId = ref(null);

// Filtros y Ordenamiento
const filterStore = ref('all');
const sortOrder = ref('asc');
const minPrice = ref(null);
const maxPrice = ref(null);

const normalizeString = (str) => {
    if (!str) return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
};

const filteredResults = computed(() => {
    let list = [...results.value];

    // Filtro por tienda con normalización de acentos
    if (filterStore.value !== 'all') {
        const targetStore = normalizeString(filterStore.value);
        list = list.filter(p => normalizeString(p.store) === targetStore);
    }

    // Filtro por rango de precio
    if (minPrice.value !== null && minPrice.value !== '') {
        const min = parseFloat(minPrice.value);
        if (!isNaN(min)) list = list.filter(p => p.price >= min);
    }
    if (maxPrice.value !== null && maxPrice.value !== '') {
        const max = parseFloat(maxPrice.value);
        if (!isNaN(max)) list = list.filter(p => p.price <= max);
    }

    // Ordenamiento
    list.sort((a, b) => {
        return sortOrder.value === 'asc' ? a.price - b.price : b.price - a.price;
    });

    return list;
});

const loadById = async (id) => {
    if (intervalId.value) clearInterval(intervalId.value);
    taskId.value = id;
    status.value = 'searching';
    results.value = [];

    // 1. Verificar si ya tenemos los datos en el store (navegación desde Historial)
    if (searchStore.currentTaskId === id && searchStore.results.length > 0) {
        results.value = searchStore.results;
        status.value = 'completed';
        return;
    }

    // 2. Si es un refresh, intentar encontrar el ID en el historial guardado
    try {
        const history = await userService.getHistory();
        const item = history.find(h => h._id === id || h.job_id === id);
        if (item && item.result?.data) {
            results.value = item.result.data;
            status.value = 'completed';
            return;
        }
    } catch (err) {
        console.warn("No se pudo recuperar el historial para recarga:", err);
    }

    // 3. Si no está en historial, asumimos que es una tarea de Celery activa
    await startPolling();
}

onMounted(async () => {
    if (route.params.id) {
        await loadById(route.params.id);
    }
});

// Watch para cambios de ID en la URL (Navegación entre resultados)
watch(() => route.params.id, async (newId) => {
    if (newId) {
        await loadById(newId);
    } else {
        // Si ya no hay ID, limpiamos el estado si era una navegación limpia a /search
        taskId.value = null;
        results.value = [];
        status.value = 'idle';
        if (intervalId.value) clearInterval(intervalId.value);
    }
});

const startSearch = async () => {
    if (!query.value) return;

    // Si estábamos viendo un resultado del historial, reiniciamos la ruta
    if (route.params.id) {
        router.push('/search');
    }

    status.value = 'searching';
    results.value = [];
    searchStore.clearResults();

    try {
        const data = await searchService.search(query.value);
        // El backend retorna job_id
        taskId.value = data.job_id;
        startPolling();
    } catch (err) {
        status.value = 'error';
        console.error(err);
    }
};

const startPolling = async () => {
    if (intervalId.value) clearInterval(intervalId.value);
    let error404Count = 0;

    // Función interna para chequear el estado
    const checkStatus = async () => {
        try {
            const data = await searchService.getTaskStatus(taskId.value);
            error404Count = 0; // Reiniciar si logramos contactar al servidor satisfactoriamente

            // Si el status es completed o tiene data
            if (data.status === 'completed' || (data.data && Array.isArray(data.data))) {
                results.value = data.data || [];
                status.value = 'completed';
                if (intervalId.value) clearInterval(intervalId.value);
                return true;
            }
            // Si el status es failed o unknown
            else if (data.status === 'failed' || data.status === 'unknown') {
                status.value = 'error';
                if (intervalId.value) clearInterval(intervalId.value);
                return true;
            }
            // Si sigue pendiente o procesando, mantenemos status 'searching'
            status.value = 'searching';
            return false;
        } catch (err) {
            // Si es un 404, puede ser que Celery aún no haya registrado la tarea en el backend
            // de resultados. En este caso mantenemos la búsqueda activa por un tiempo.
            if (err.response && err.response.status === 404) {
                error404Count++;
                if (error404Count < 10) { // Reintentar por ~20 segundos
                    console.warn(`Tarea ${taskId.value} aún no disponible (404). Reintento ${error404Count}...`);
                    status.value = 'searching';
                    return false;
                }
            }
            console.error(err);
            status.value = 'error';
            if (intervalId.value) clearInterval(intervalId.value);
            return true;
        }
    };

    // Ejecución inicial por si ya está listo (historial)
    const finished = await checkStatus();
    if (finished) return;

    // Si no está listo, iniciamos el intervalo
    intervalId.value = setInterval(checkStatus, 2000);
};

const logout = () => {
    auth.logout();
    router.push('/');
};

onUnmounted(() => {
    if (intervalId.value) clearInterval(intervalId.value);
});
</script>

<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navbar -->
        <nav class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16 items-center">
                    <div class="flex items-center space-x-2">
                        <span class="text-2xl">🕷️</span>
                        <span class="text-xl font-bold text-gray-900 leading-none">WebScraping Pro</span>
                    </div>
                    <div class="flex items-center space-x-4">
                        <router-link to="/history"
                            class="text-gray-600 hover:text-green-600 flex items-center space-x-1">
                            <HistoryIcon :size="20" />
                            <span>Historial</span>
                        </router-link>
                        <button @click="logout" class="text-gray-600 hover:text-red-600 flex items-center space-x-1">
                            <LogOut :size="20" />
                            <span>Salir</span>
                        </button>
                    </div>
                </div>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Search Bar -->
            <div class="max-w-3xl mx-auto mb-12">
                <div class="relative group">
                    <input v-model="query" type="text"
                        placeholder="¿Qué producto buscas hoy? (ej: iPhone, televisor...)"
                        class="w-full pl-12 pr-32 py-4 bg-white border-2 border-gray-200 rounded-2xl focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all outline-none text-lg shadow-sm"
                        @keyup.enter="startSearch" />
                    <Search
                        class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-green-500 transition-colors"
                        :size="24" />
                    <button @click="startSearch" :disabled="status === 'searching'"
                        class="absolute right-3 top-1/2 -translate-y-1/2 bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-xl font-semibold transition-colors disabled:bg-gray-300">
                        {{ status === 'searching' ? 'Buscando...' : 'Buscar' }}
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="status === 'searching'" class="flex flex-col items-center justify-center py-20 space-y-4">
                <Loader2 class="animate-spin text-green-500" :size="48" />
                <p class="text-gray-600 font-medium">Estamos consultando Éxito y Alkosto para ti...</p>
            </div>

            <!-- Filtros -->
            <div v-if="status === 'completed' && results.length > 0"
                class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
                <div class="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-6">
                    <!-- Tienda -->
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Comercio</label>
                        <div class="relative">
                            <select v-model="filterStore"
                                class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 appearance-none focus:ring-2 focus:ring-green-100 focus:border-green-500 outline-none transition-all">
                                <option value="all">Todos los comercios</option>
                                <option value="exito">Éxito</option>
                                <option value="alkosto">Alkosto</option>
                            </select>
                            <Filter class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
                                :size="16" />
                        </div>
                    </div>

                    <!-- Precio -->
                    <div class="flex-2">
                        <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Rango de Precio</label>
                        <div class="flex items-center space-x-2">
                            <input v-model.number="minPrice" type="number" placeholder="Min"
                                class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 focus:border-green-500 outline-none transition-all" />
                            <span class="text-gray-400">-</span>
                            <input v-model.number="maxPrice" type="number" placeholder="Max"
                                class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 focus:border-green-500 outline-none transition-all" />
                        </div>
                    </div>

                    <!-- Ordenar -->
                    <div class="flex-1">
                        <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Ordenar por precio</label>
                        <div class="relative">
                            <select v-model="sortOrder"
                                class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 appearance-none focus:ring-2 focus:ring-green-100 focus:border-green-500 outline-none transition-all">
                                <option value="asc">Menor a Mayor</option>
                                <option value="desc">Mayor a Menor</option>
                            </select>
                            <ArrowUpDown
                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
                                :size="16" />
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="status === 'completed' && filteredResults.length > 0"
                class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                <div v-for="product in filteredResults" :key="product.url"
                    class="bg-white rounded-2xl border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow group">
                    <div class="aspect-square bg-gray-100 relative overflow-hidden">
                        <img :src="product.image" :alt="product.name"
                            class="w-full h-full object-cover group-hover:scale-105 transition-transform" />
                        <div
                            class="absolute top-2 right-2 bg-white/90 backdrop-blur px-2 py-1 rounded-lg text-xs font-bold shadow-sm">
                            {{ product.store.toUpperCase() }}
                        </div>
                    </div>
                    <div class="p-4 flex flex-col items-start h-40">
                        <h3 class="font-semibold text-gray-800 line-clamp-2 mb-2 text-sm h-10">{{ product.name }}</h3>
                        <div class="mt-auto w-full">
                            <p class="text-2xl font-bold text-green-600 mb-3">${{ product.price.toLocaleString() }}</p>
                            <a :href="product.url" target="_blank"
                                class="w-full flex items-center justify-center space-x-2 bg-gray-50 hover:bg-green-50 text-gray-700 hover:text-green-700 py-2 rounded-xl transition-colors border border-gray-100">
                                <span>Ver en tienda</span>
                                <ExternalLink :size="16" />
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="status === 'completed' && results.length === 0" class="text-center py-20">
                <p class="text-gray-500 text-lg">No encontramos resultados para tu búsqueda. Prueba con otros términos.
                </p>
            </div>
        </main>
    </div>
</template>
