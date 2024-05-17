<template>
  <div>
    <h1>주택담보대출</h1>

    <!-- 은행 선택 버튼 -->
    <select class="form-select form-select-lg mb-3" aria-label="Large select example" v-model="selectedBank">
      <option class="selected" value="all">전체 은행</option>
      <option 
        v-for="bank in loanStore.banks"
        :key="bank.kor_co_nm"
        :bank="bank.kor_co_nm"
      >
        {{ bank }}
      </option>
    </select>


    <!-- 표 -->
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">번호</th>
          <th scope="col">공시제출일</th>
          <th scope="col">금융회사명</th>
          <th scope="col">상품명</th>
          <th scope="col" @click="sort(6)">대출금리유형</th>
          <th scope="col" @click="sort(12)">최저 대출금리 (Click to sort↑)</th>
          <th scope="col" @click="sort(24)">최고 대출금리 (Click to sort↑)</th>
          <th scope="col" @click="sort(36)">전월 취급 평균금리 (Click to sort↑)</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(prd, index) in loanStore.loans"
          :key="prd.id"
          data-bs-toggle="modal" data-bs-target="#exampleModal"
          @click="model(prd)"
        >
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ prd.dcls_month }}</td>
          <td>{{ prd.kor_co_nm }}</td>
          <td>{{ prd.fin_prdt_nm }}</td>
          <td>{{ prd.loanoption_set.rpay_type_nm }}</td>
          <td>{{ prd.loanoption_set.lend_rate_avg }}</td>
          <td>{{ prd.loanoption_set.lend_rate_max }}</td>
          <td>{{ prd.loanoption_set.lend_rate_min }}</td>
        </tr>
      </tbody>
    </table>


    <!-- 모달 -->
    <div v-if="loan" class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{loan.fin_prdt_nm}}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            {{ loan }}
          </div>

          <!-- 가입신청 / 관심상품 저장 버튼 -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" v-if="isContracted" @click="delContract(loan.fin_prdt_cd)">
              가입 취소
            </button>
            <button type="button" class="btn btn-danger" v-else @click="addContract(loan)">
              가입 신청
            </button>

            <!-- <button type="button" class="btn btn-primary" v-if="isSaved" @click="delSave(prd.id)">
              관심상품 저장
            </button>
            <button type="button" class="btn btn-danger" v-else @click="addSave(prd)">
              저장 취소
            </button> -->

          </div>
        </div>
      </div>
    </div>

  </div>
  
</template>

<script setup>
import { useLoanStore } from '@/stores/loan.js'
import { useAuthStore } from '@/stores/auth.js'
import { ref, watch, computed, onMounted } from 'vue'
import axios from 'axios'

const loanStore = useLoanStore()
const authStore = useAuthStore()

// 전체 조회
loanStore.getAll()

console.log(loanStore.loan)

// 특정 저축 기간에 대한 이자율 찾는 함수
const getInterestRate = (prd, term) => {
  const option = prd.loanoption_set.find(option => option.save_trm === term)
  return option ? option.intr_rate : '-'
}


// 특정 은행 선택 시 조회
const selectedBank = ref('all')

// selectedBank 값이 변경될 때마다 데이터 갱신
watch(selectedBank, (newValue) => {
  if (newValue === 'all') {
    loanStore.getAll()
  } else {
    loanStore.selectBank(selectedBank.value)
  }
})


// 기간 선택 시 정렬
const sort = function(num) {
  axios({
    method: 'get',
    url: `${loanStore.API_URL}/fin_products/loan/des_sort/${selectedBank}/${save_trm}/`,
  })
    .then(response => {
      loanStore.loans.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
}


// 모달
const loan = ref({})

const model = function(prd) {
  loan.value = prd
}


// 가입한 상품 조회
const getContract = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${loanStore.API_URL}/fin_products/loan_contract/${loan.value.fin_prdt_cd}/`
    })
      .then(response => {
        loanStore.contractedLoan.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }
onMounted(() => {
  if (loanStore.contractedLoan.length !== 0) {
    getContract()
  }
})


// 상품이 계약됐는지 판단
const isContracted = computed(() => {
  if (loanStore.contractedLoan.length === 0) {
    return false
  } 
  const findPrd = loanStore.contractedLoan.findIndex((prd) => prd.fin_prdt_cd === loan.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  console.log(loanStore.contractedLoan)
  return false
})


// 상품 계약
const addContract = (prd) => {
  loanStore.contractedLoan.push(prd)

  axios({
      method: 'post',
      url: `${loantStore.API_URL}/fin_products/loan_contract/${loan.value.fin_prdt_cd}/`,
      data: {
        code: loan.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        loanStore.contractedLoan.push(loan)
      })
      .catch(error => {
        console.log(error)
      })

  }
  

// 상품 계약 취소
const delContract = (fin_prdt_cd) => {
  const idx = loanStore.contractedLoan.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  console.log(`${loanStore.API_URL}/fin_products/loan_contract/${loan.value.fin_prdt_cd}/`)
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan_contract/${loan.value.fin_prdt_cd}/`,
      data: {
        code: loan.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        loanStore.contractedLoan.splice(idx, 1) 
      })
      .catch(error => {
        console.log(error)
      })
  }
}


</script>


<style scoped>

</style>
