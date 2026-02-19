import { defineStore } from "pinia";

export const useSearchStore = defineStore("search", {
  state: () => ({
    results: [],
    metadata: [],
    totalTime: 0,
    currentTaskId: null,
  }),
  actions: {
    setResults(data, metadata = [], totalTime = 0, taskId = null) {
      this.results = data;
      this.metadata = metadata;
      this.totalTime = totalTime;
      this.currentTaskId = taskId;
    },
    clearResults() {
      this.results = [];
      this.metadata = [];
      this.totalTime = 0;
      this.currentTaskId = null;
    },
  },
});
