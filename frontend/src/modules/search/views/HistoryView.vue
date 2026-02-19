<script setup>
import { ref, onMounted, computed } from 'vue';
import { userService } from '../../../api';
import { History as HistoryIcon, ArrowLeft, Calendar, ExternalLink, Loader2, Filter, ArrowUpDown, ChevronDown, ChevronUp } from 'lucide-vue-next';
import { useSearchStore } from '../../../stores/search';
import { useRouter } from 'vue-router';

const history = ref([]);
const loading = ref(true);
const expandedItem = ref(null);
const searchStore = useSearchStore();
const router = useRouter();

// Filtros para el ítem expandido
const filterStore = ref('all');
const sortOrder = ref('asc');
const minPrice = ref(null);
const maxPrice = ref(null);

const normalizeString = (str) => {
    if (!str) return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
};

const toggleExpand = (id) => {
    if (expandedItem.value === id) {
        expandedItem.value = null;
    } else {
        expandedItem.value = id;
        // Reset filtros al expandir uno nuevo
        filterStore.value = 'all';
        sortOrder.value = 'asc';
        minPrice.value = null;
        maxPrice.value = null;
    }
};

const filteredExpandedProducts = computed(() => {
    const item = history.value.find(h => h._id === expandedItem.value);
    if (!item || !item.result?.data) return [];

    let list = [...item.result.data];

    // Filtro por tienda
    if (filterStore.value !== 'all') {
        const targetStore = normalizeString(filterStore.value);
        list = list.filter(p => normalizeString(p.store) === targetStore);
    }

    // Filtros de precio
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

const goToResults = (item) => {
    // Usamos el store para pasar los datos directamente
    searchStore.setResults(
        item.result.data,
        item.result.metadata,
        item.result.total_time,
        item._id // Usamos el ID de Mongo
    );
    router.push(`/search/result/${item._id}`);
};

const formatDate = (dateStr) => {
    if (!dateStr) return 'Fecha desconocida';
    return new Date(dateStr).toLocaleString();
};

onMounted(async () => {
    try {
        const data = await userService.getHistory();
        history.value = data || [];
    } catch (err) {
        console.error('Error fetching history:', err);
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="min-h-screen bg-gray-50 p-6">
        <div class="max-w-5xl mx-auto">
            <div class="flex items-center justify-between mb-8">
                <div class="flex items-center space-x-4">
                    <router-link to="/search" class="p-2 hover:bg-white rounded-full transition-colors text-gray-600">
                        <ArrowLeft :size="24" />
                    </router-link>
                    <h1 class="text-3xl font-bold text-gray-900 flex items-center space-x-3">
                        <HistoryIcon class="text-green-500" :size="32" />
                        <span>Tu Historial de Búsquedas</span>
                    </h1>
                </div>
            </div>

            <div v-if="loading" class="text-center py-20">
                <Loader2 class="animate-spin text-green-500 mx-auto mb-4" :size="48" />
                <p class="text-gray-500">Cargando tu historial...</p>
            </div>

            <div v-else class="space-y-4">
                <div v-for="item in history" :key="item._id"
                    class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:border-green-200 transition-all">
                    <div class="flex justify-between items-start mb-4">
                        <div class="cursor-pointer group flex-1" @click="goToResults(item)">
                            <div class="flex items-center space-x-2">
                                <h3
                                    class="text-xl font-bold text-gray-800 group-hover:text-green-600 transition-colors">
                                    "{{ item.search_query }}"</h3>
                                <ExternalLink class="text-gray-300 group-hover:text-green-500" :size="16" />
                            </div>
                            <div class="flex items-center space-x-2 text-sm text-gray-500">
                                <Calendar :size="14" />
                                <span>Realizada el {{ formatDate(item.created_at) }}</span>
                            </div>
                        </div>
                        <div class="flex space-x-2">
                            <span v-for="meta in item.result?.metadata" :key="meta.store_name"
                                class="px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-bold uppercase transition-transform hover:scale-105">
                                {{ meta.store_name }} ({{ meta.count }})
                            </span>
                        </div>
                    </div>

                    <div v-if="item.result?.data">
                        <!-- Filtros (Solo visibles si el ítem está expandido) -->
                        <div v-if="expandedItem === item._id"
                            class="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4 bg-gray-50 p-4 rounded-xl border border-gray-200">
                            <div>
                                <label class="block text-[10px] font-bold text-gray-500 uppercase mb-1">Comercio</label>
                                <select v-model="filterStore"
                                    class="w-full text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-green-100 focus:border-green-500 outline-none">
                                    <option value="all">Todos</option>
                                    <option value="exito">Éxito</option>
                                    <option value="alkosto">Alkosto</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-gray-500 uppercase mb-1">Precio (Min -
                                    Max)</label>
                                <div class="flex items-center space-x-2">
                                    <input v-model.number="minPrice" type="number" placeholder="0"
                                        class="w-full text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:border-green-500 outline-none" />
                                    <input v-model.number="maxPrice" type="number" placeholder="Max"
                                        class="w-full text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:border-green-500 outline-none" />
                                </div>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-gray-500 uppercase mb-1">Orden</label>
                                <select v-model="sortOrder"
                                    class="w-full text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-green-100 focus:border-green-500 outline-none">
                                    <option value="asc">Menor a Mayor</option>
                                    <option value="desc">Mayor a Menor</option>
                                </select>
                            </div>
                        </div>

                        <!-- Vista de cuadrícula -->
                        <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-7 gap-3">
                            <!-- Si está expandido, usamos la lista filtrada. Si no, los primeros 5 -->
                            <a v-for="prod in (expandedItem === item._id ? filteredExpandedProducts : item.result.data.slice(0, 5))"
                                :key="prod.url" :href="prod.url" target="_blank"
                                class="aspect-square bg-gray-50 rounded-lg overflow-hidden border border-gray-100 hover:ring-2 hover:ring-green-500 transition-all relative group shadow-sm">
                                <img :src="prod.image"
                                    class="w-full h-full object-cover group-hover:scale-110 transition-transform" />
                                <div
                                    class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                                    <ExternalLink class="text-white" :size="20" />
                                </div>
                                <div
                                    class="absolute bottom-0 left-0 right-0 bg-white/90 text-[10px] font-bold p-1 truncate">
                                    ${{ prod.price.toLocaleString() }}
                                </div>
                                <div v-if="expandedItem === item._id"
                                    class="absolute top-0 left-0 bg-green-500 text-white text-[8px] px-1 font-bold rounded-br-lg">
                                    {{ prod.store.toUpperCase() }}
                                </div>
                            </a>

                            <!-- Botón para expandir si hay más de 5 elementos y no está expandido -->
                            <button v-if="item.result.data.length > 5 && expandedItem !== item._id"
                                @click="toggleExpand(item._id)"
                                class="aspect-square bg-gray-100 rounded-lg flex flex-col items-center justify-center text-gray-500 hover:bg-gray-200 transition-colors group">
                                <span class="font-bold text-lg text-gray-600">+{{ item.result.data.length - 5 }}</span>
                                <span class="text-[10px] font-medium uppercase text-center px-1">Ver todos y
                                    filtrar</span>
                            </button>

                            <!-- Botón para cerrar/contraer -->
                            <button v-if="expandedItem === item._id" @click="toggleExpand(item._id)"
                                class="aspect-square bg-green-50 rounded-lg flex flex-col items-center justify-center text-green-600 hover:bg-green-100 transition-colors ring-2 ring-green-500 ring-inset">
                                <ChevronUp :size="24" />
                                <span class="text-[10px] font-bold uppercase">Cerrar</span>
                            </button>
                        </div>

                        <!-- Info de resultados filtrados cuando está expandido -->
                        <p v-if="expandedItem === item._id" class="mt-4 text-xs font-medium text-gray-400">
                            Mostrando {{ filteredExpandedProducts.length }} de {{ item.result.data.length }} productos.
                            <span v-if="filteredExpandedProducts.length === 0" class="text-red-400 ml-2">No hay
                                resultados
                                con estos filtros.</span>
                        </p>
                    </div>
                </div>

                <div v-if="history.length === 0"
                    class="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-gray-200">
                    <p class="text-gray-400 text-lg">Aún no has realizado ninguna búsqueda.</p>
                    <router-link to="/search" class="mt-4 inline-block text-green-600 font-bold hover:underline">Empieza
                        a buscar ahora</router-link>
                </div>
            </div>
        </div>
    </div>
</template>
