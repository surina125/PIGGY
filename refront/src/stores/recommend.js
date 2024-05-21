import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useRecommendStore = defineStore('recommend', () => {
  const deposits = ref([])
  const deposits_period = ref("")
  
  const savings = ref([])
  const savings_type = ref("")
  const savings_period = ref("")



  return { deposits, deposits_period, savings, savings_type, savings_period }
}, { persist: true })
