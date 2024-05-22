import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useLoanStore = defineStore('loan', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const loans = ref([])
  const banks = ref([])
  const Aloans = ref([])
  const Eloans = ref([])


  // dcls_month = ref("")                                                       
  // fin_co_no = ref("")                                                    
  // kor_co_nm = ref("")                                         
  // fin_prdt_cd = ref("")                                       
  // fin_prdt_nm = ref("")                                                 
  // join_way = ref("")                                                      
  // erly_rpay_fee = ref("")                                                
  // dly_rate = ref("")                                                                     
  // loan_lmt = ref("")                                                                 
  // lend_rate_type_nm = ref("")
  // lend_rate_min = ref(0)
  // lend_rate_max = ref(0)
  // lend_rate_avg = ref(0)


  // 전체 데이터 저장
  const getAll = function() {
    axios({
      method: 'get',
      url: `${API_URL}/fin_products/loans/all_bank/all_type/`
    })
      .then(response => {
        loans.value = response.data
        console.log(loans)

        loans.value.forEach(loan => {
          const bankName = loan.kor_co_nm
          
          // 이미 저장된 은행인지 확인하고 중복되지 않는 경우에만 추가
          if (!banks.value.includes(bankName)) {
            banks.value.push(bankName)
          }
        

          // loanoption_set 배열을 순회
          if (loan.loanoption_set) {
            loan.loanoption_set.forEach(option => {
              // 각 옵션에 대해 필요한 작업 수행
              // console.log(option)

              if (option.mrtg_type_nm==="아파트") {
                // lend_rate_type_nm.value = option.lend_rate_type_nm
                // lend_rate_min.value = option.lend_rate_min
                // lend_rate_max.value = option.lend_rate_max
                // lend_rate_avg.value = option.lend_rate_avg

                Aloans.value.push({
                  mrtg_type_nm: bankName,
                  dcls_month: loan.dcls_month,
                  fin_co_no: loan.fin_co_no,
                  fin_prdt_nm: loan.fin_prdt_nm,
                  kor_co_nm: loan.kor_co_nm,
                  fin_prdt_cd: loan.fin_prdt_cd,
                  join_way: loan.join_way,
                  erly_rpay_fee: loan.erly_rpay_fee,
                  dly_rate: loan.dly_rate,
                  // loan_lmt: loan.loan_lmt,
                  // mrtg_type_nm: option.mrtg_type_nm,
                  // rpay_type_nm: option.rpay_type_nm,
                  lend_rate_type_nm: option.lend_rate_type_nm,
                  lend_rate_min: option.lend_rate_min,
                  lend_rate_max: option.lend_rate_max,
                  lend_rate_avg: option.lend_rate_avg,
                })

              } else if (option.mrtg_type_nm==="아파트외") {
                // lend_rate_type_nm.value = option.lend_rate_type_nm
                // lend_rate_min.value = option.lend_rate_min
                // lend_rate_max.value = option.lend_rate_max
                // lend_rate_avg.value = option.lend_rate_avg

                Eloans.value.push({
                  mrtg_type_nm: bankName,
                  dcls_month: loan.dcls_month,
                  fin_co_no: loan.fin_co_no,
                  kor_co_nm: loan.kor_co_nm,
                  fin_prdt_nm: loan.fin_prdt_nm,
                  fin_prdt_cd: loan.fin_prdt_cd,
                  join_way: loan.join_way,
                  erly_rpay_fee: loan.erly_rpay_fee,
                  dly_rate: loan.dly_rate,
                  // loan_lmt: loan.loan_lmt,
                  // mrtg_type_nm: option.mrtg_type_nm,
                  // rpay_type_nm: option.rpay_type_nm,
                  lend_rate_type_nm: option.lend_rate_type_nm,
                  lend_rate_min: option.lend_rate_min,
                  lend_rate_max: option.lend_rate_max,
                  lend_rate_avg: option.lend_rate_avg,
                })
              
              }
            });
          }
        });
    })
      .catch(error => {
        console.log(error)
      })
  }


  // 가입한 예금 저장
  const contractedLoan = ref([])

  // 관심 예금 저장
  const savedLoan = ref([])

  const selectedLoans = ref([])


  return { API_URL, loans, Aloans, Eloans, getAll, banks, contractedLoan, savedLoan, selectedLoans }
}, { persist: true })
