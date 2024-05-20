import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useRecommendStore = defineStore('recommend', () => {
  const deposits = ref([])


  return { deposits }
}, { persist: true })
