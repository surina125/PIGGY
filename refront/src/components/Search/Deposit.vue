<template>
  <div>
    <h1>정기예금</h1>

    <!-- 은행 선택 버튼 -->
    <select class="form-select form-select-lg mb-3" aria-label="Large select example" v-model="selectedBank">
      <option class="selected" value="all_bank">전체 은행</option>
      <option 
        v-for="bank in depositStore.banks"
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
          <th scope="col" @click="sort('6')">6개월 (Click to sort↓)</th>
          <th scope="col" @click="sort('12')">12개월 (Click to sort↓)</th>
          <th scope="col" @click="sort('24')">24개월 (Click to sort↓)</th>
          <th scope="col" @click="sort('36')">36개월 (Click to sort↓)</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(prd, index) in depositStore.deposits"
          :key="index"
          data-bs-toggle="modal" data-bs-target="#exampleModal"
          @click="model_click(prd)"
        >
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ prd.dcls_month }}</td>
          <td>{{ prd.kor_co_nm }}</td>
          <td>{{ prd.fin_prdt_nm }}</td>
          <td>{{ getInterestRate(prd, '6') }}</td>
          <td>{{ getInterestRate(prd, '12') }}</td>
          <td>{{ getInterestRate(prd, '24') }}</td>
          <td>{{ getInterestRate(prd, '36') }}</td>
        </tr>
      </tbody>
    </table>


    <!-- 모달 -->
    <div v-if="deposit" class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{deposit.fin_prdt_nm}}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <table class="table table-hover">
              <tbody>
                <tr>
                  <th class="modal_row" scope="row">공시제출일</th>
                  <td>{{ deposit.dcls_month }}</td>
                </tr>
                <tr>
                  <th scope="row">금융회사명</th>
                  <td>{{ deposit.kor_co_nm }}</td>
                </tr>
                <tr>
                  <th scope="row">가입방법</th>
                  <td>{{ deposit.join_way }}</td>
                </tr>
                <tr>
                  <th scope="row">가입대상</th>
                  <td>{{ deposit.join_member }}</td>
                </tr>
                <tr>
                  <th scope="row">최고 한도</th>
                  <td>{{ deposit.max_limit }}</td>
                </tr>
                <tr>
                  <th scope="row">만기 후 이자율</th>
                  <td>{{ deposit.mtrt_int }}</td>
                </tr>
                <tr>
                  <th scope="row">우대조건</th>
                  <td>{{ deposit.spcl_cnd }}</td>
                </tr>
                <tr>
                  <th scope="row">기타 유의사항</th>
                  <td>{{ deposit.etc_note }}</td>
                </tr>
              </tbody>
            </table>

            <!-- 차트 -->
            <!-- <DepositChart/> -->
          </div>

          <!-- 가입신청 / 관심상품 저장 버튼 -->
          <div v-if="authStore.isAuthenticated" class="modal-footer no-border">
            <button type="button" class="btn btn-danger" v-if="isContracted" @click="delContract(deposit.fin_prdt_cd)">
              가입 취소
            </button>
            <button type="button" class="btn btn-primary" v-else @click="addContract(deposit)">
              가입 신청
            </button>

            <button type="button" class="btn btn-danger" v-if="isSaved" @click="delSave(deposit.fin_prdt_cd)">
              관심상품 저장
            </button>
            <button type="button" class="btn btn-primary" v-else @click="addSave(deposit)">
              저장 취소
            </button>
          </div>
          
        </div>
      </div>
    </div>

  </div>
  
</template>

<script setup>
import { useDepositStore } from '@/stores/deposit.js'
import { useAuthStore } from '@/stores/auth.js'
import { ref, watch, computed, onMounted } from 'vue'
import axios from 'axios'
// import DepositChart from '@/components/Chart/DepositChart.vue'

const depositStore = useDepositStore()
const authStore = useAuthStore()

// 전체 조회
depositStore.getAll()

// 특정 저축 기간에 대한 이자율 찾는 함수
const getInterestRate = (prd, term) => {
  const option = prd.depositoption_set.find(option => option.save_trm === term)
  return option ? option.intr_rate : '-'
}


// 특정 은행 선택 시 조회
const selectedBank = ref('all_bank')

// selectedBank 값이 변경될 때마다 데이터 갱신
watch(selectedBank, (newValue) => {
  if (newValue === 'all') {
    depositStore.getAll()
  } else {
    depositStore.selectBank(selectedBank.value)
  }
})

// selectedBank 값이 변경될 때마다 데이터 갱신
watch(selectedBank, (newValue) => {
  if (newValue === 'all') {
    depositStore.getAll()
  } else {
    depositStore.selectBank(selectedBank.value)
  }
})


// 기간 선택 시 정렬
const sort = function(num) {
  axios({
    method: 'get',
    url: `${depositStore.API_URL}/fin_products/deposit/bank/${selectedBank.value}/sort/${num}/`,
  })
    .then(response => {
      depositStore.deposits = response.data
    })
    .catch(error => {
      console.log(error)
    })
}


// 모달
const deposit = ref({})

const model_click = function(prd) {
  deposit.value = prd
  depositStore.forChartDeposit = prd
  console.log(depositStore.forChartDeposit)
}


// 가입한 상품 조회
const getContract = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${depositStore.API_URL}/fin_products/deposit_contract/${deposit.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        depositStore.contractedDeposit = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }
onMounted(() => {
  if (authStore.isAuthenticated && depositStore.contractedDeposit.length !== 0 && deposit.value.fin_prdt_cd) {
    getContract()
  }
})


// 상품이 계약됐는지 판단
const isContracted = computed(() => {
  if (depositStore.contractedDeposit.length === 0) {
    return false
  } 
  const findPrd = depositStore.contractedDeposit.findIndex((prd) => prd.fin_prdt_cd === deposit.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  return false
})


// 상품 계약
const addContract = (prd) => {
  depositStore.contractedDeposit.push(prd)

  axios({
      method: 'post',
      url: `${depositStore.API_URL}/fin_products/deposit/contract/${deposit.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: deposit.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        depositStore.contractedDeposit.push(deposit)
      })
      .catch(error => {
        console.log(error)
      })

  }
  

// 상품 계약 취소
const delContract = (fin_prdt_cd) => {
  const idx = depositStore.contractedDeposit.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${depositStore.API_URL}/fin_products/deposit/contract/${deposit.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: deposit.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        depositStore.contractedDeposit.splice(idx, 1) 
      })
      .catch(error => {
        console.log(error)
      })
  }
}



// 관심상품 조회
const getSave = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${depositStore.API_URL}/fin_products/deposit/like/${deposit.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        depositStore.savedDeposit = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }
onMounted(() => {
  if (authStore.isAuthenticated && depositStore.savedDeposit.length !== 0 && deposit.value.fin_prdt_cd) {
    getSave()
  }
})


// 관심상품 저장하고 있는지 판단
const isSaved = computed(() => {
  if (depositStore.savedDeposit.length === 0) {
    return false
  } 
  const findPrd = depositStore.savedDeposit.findIndex((prd) => prd.fin_prdt_cd === deposit.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  return false
})


// 관심상품 저장
const addSave = (prd) => {
  depositStore.savedDeposit.push(prd)

  axios({
      method: 'post',
      url: `${depositStore.API_URL}/fin_products/deposit/like/${deposit.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: deposit.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        depositStore.savedDeposit.push(deposit)
      })
      .catch(error => {
        console.log(error)
      })

  }
  

// 관심상품 저장 취소
const delSave = (fin_prdt_cd) => {
  const idx = depositStore.savedDeposit.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${depositStore.API_URL}/fin_products/deposit/like/${deposit.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: deposit.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        depositStore.savedDeposit.splice(idx, 1) 
      })
      .catch(error => {
        console.log(error)
      })
  }
}
</script>


<style scoped>
.modal_row {
  width: 150px;
}
.no-border {
  border: none;
}
</style>
