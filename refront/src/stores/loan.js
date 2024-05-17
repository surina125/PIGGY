import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useLoanStore = defineStore('loan', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const loans = ref([])
  const banks = ref([])

  // 전체 데이터 저장
  const getAll = function() {
    axios({
      method: 'get',
      url: `${API_URL}/fin_products/loan/`
    })
      .then(response => {
        loans.value = response.data

        // 각 은행을 확인하고 저장
        loans.value.forEach(loan => {
          const bankName = loan.kor_co_nm
          // 이미 저장된 은행인지 확인하고 중복되지 않는 경우에만 추가
          if (!banks.value.includes(bankName)) {
            banks.value.push(bankName)
          }
        })
      })
      .catch(error => {
        console.log(error)
      })
  }


  // 특정 은행 선택 시 데이터 저장
  const selectBank = function(kor_co_nm) {
    axios({
      method: 'get',
      url: `${API_URL}/fin_products/loan/bank/${kor_co_nm}/`
    })
      .then(response => {
        loans.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }


  // 가입한 예금 저장
  const contractedLoan = ref([])

  // 관심 예금 저장
  const savedLoan = ref([])


  return { API_URL, loans, getAll, banks, selectBank, contractedLoan, savedLoan }
}, { persist: true })
