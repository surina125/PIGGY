import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'


export const useRecommendStore = defineStore('recommend', () => {
  // 두번째 추천 방법에서 필요
  const deposits = ref([])
  const deposits_period = ref("")
  
  const savings = ref([])
  const savings_type = ref("")
  const savings_period = ref("")

  const loas = ref([])
  const loas_type = ref("")

  // 첫번째 추천 방법에서 필요
  const authStore = useAuthStore()
  const reco1D = ref([])
  const reco1S = ref([])
  const reco1L = ref([])

  const reco1Result = function () {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/users/recommend/${authStore.userData.username}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then(response => {
      const dProducts = response.data.D_products // D_products 배열
      const sProducts = response.data.S_products // S_products 배열
      const lProducts = response.data.L_products // S_products 배열
  
      // D_products 배열을 순회하면서 세부 정보를 가져오기
      dProducts.forEach(productId => {
        axios({
          method: 'get',
          url: `http://127.0.0.1:8000/fin_products/deposit/${productId}/`,
          headers: {
            Authorization: `Token ${authStore.token}`
          }
        })
        .then(productResponse => {
          reco1D.value.push(productResponse.data)
        })
        .catch(error => {
          console.log(error)
        })
      })
  
      // S_products 배열을 순회하면서 세부 정보를 가져오기
      sProducts.forEach(productId => {
        axios({
          method: 'get',
          url: `http://127.0.0.1:8000/fin_products/savings/${productId}/`,
          headers: {
            Authorization: `Token ${authStore.token}`
          }
        })
        .then(productResponse => {
          reco1S.value.push(productResponse.data)
        })
        .catch(error => {
          console.log(error)
        })
      })

      // L_products 배열을 순회하면서 세부 정보를 가져오기
      lProducts.forEach(productId => {
        axios({
          method: 'get',
          url: `http://127.0.0.1:8000/fin_products/loans/${productId}/`,
          headers: {
            Authorization: `Token ${authStore.token}`
          }
        })
        .then(productResponse => {
          reco1L.value.push(productResponse.data)
        })
        .catch(error => {
          console.log(error)
        })
      })


    })
    .catch(error => {
      console.log(error)
    })
  }



  return { deposits, deposits_period, savings, savings_type, savings_period, loas, loas_type, reco1Result, reco1D, reco1S, reco1L }
}, { persist: true })
