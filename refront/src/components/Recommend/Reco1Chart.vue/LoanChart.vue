<template>
  <div>
    <!-- 표 -->
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">번호</th>
          <th scope="col">공시제출일</th>
          <th scope="col">금융회사명</th>
          <th scope="col">상품명</th>
          <th scope="col">담보유형</th>
        </tr>
      </thead>

      <!-- 담보유형 아파트인 경우 -->
      <tbody>
        <tr 
          v-for="(prd, index) in recommendStore.reco1L"
          :key="index"
          data-bs-toggle="modal" data-bs-target="#loanModal"
          @click="modal_click(prd)"
        >
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ prd.dcls_month }}</td>
          <td>{{ prd.kor_co_nm }}</td>
          <td>{{ prd.fin_prdt_nm }}</td>
          <td>{{ recommendStore.loas_type }}</td>

        </tr>
      </tbody>
    </table>


    <!-- 모달 -->
    <div v-if="loan" class="modal fade loan" id="loanModal" tabindex="-1" aria-labelledby="loanModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="loanModalLabel">{{loan.fin_prdt_nm}}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">

            <table class="table table-hover">
              <tbody>
                <tr>
                  <th class="modal_row" scope="row">공시제출일</th>
                  <td>{{ loan.dcls_month }}</td>
                </tr>
                <tr>
                  <th scope="row">금융회사명</th>
                  <td>{{ loan.kor_co_nm }}</td>
                </tr>
                <tr>
                  <th scope="row">담보유형</th>
                  <td>{{ recommendStore.loas_type }}</td>
                </tr>
                <tr>
                  <th scope="row">가입방법</th>
                  <td>{{ loan.join_way }}</td>
                </tr>
                <tr>
                  <th scope="row">중도상환수수료</th>
                  <td>{{ loan.erly_rpay_fee }}</td>
                </tr>
                <tr>
                  <th scope="row">연체 이자율</th>
                  <td>{{ loan.dly_rate }}</td>
                </tr>
                <tr>
                  <th scope="row">대출한도</th>
                  <td>{{ loan.lmt }}</td>
                </tr>

                <tr>
                  <!-- 차트 -->
                  <td v-if="loan" colspan="7">
                    <Bar v-if="recommendStore.loas_type === '아파트'" class="chart-page" :data="apartmentChartData" :options="options"/>
                    <Bar v-else class="chart-page" :data="nonApartmentChartData" :options="options"/>
                  </td>               
                </tr>
              </tbody>
            </table>


          </div>

          <!-- 가입신청 / 관심상품 저장 버튼 -->
          <div v-if="authStore.isAuthenticated" class="modal-footer no-border">
            <button type="button" class="btn btn-danger" v-if="isContracted" @click="delContract(loan.fin_prdt_cd)">
              가입 취소
            </button>
            <button type="button" class="btn btn-primary" v-else @click="addContract(loan)">
              가입 신청
            </button>

            <button type="button" class="btn btn-danger" v-if="isSaved" @click="delSave(loan.fin_prdt_cd)">
              저장 취소
            </button>
            <button type="button" class="btn btn-primary" v-else @click="addSave(loan)">
              관심상품 저장
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
  
</template>

<script setup>
import { useLoanStore } from '@/stores/loan.js'
import { useAuthStore } from '@/stores/auth.js'
import { useRecommendStore } from '@/stores/recommend'
import { ref, computed } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

const loanStore = useLoanStore()
const authStore = useAuthStore()
const recommendStore = useRecommendStore()



console.log(loanStore.Aloans)

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)


// 모달
const loan = ref({})

const modal_click = function(prd) {
  loan.value = prd

  getContract()
  getSave()

  // 아파트 담보 유형 차트 데이터 업데이트
  const apartmentData = loan.value.loanoption_set.filter(option => option.mrtg_type_nm === '아파트')
  const apartmentFixedRate = apartmentData.find(option => option.lend_rate_type_nm === '고정금리')
  const apartmentVariableRate = apartmentData.find(option => option.lend_rate_type_nm === '변동금리')

  apartmentChartData.value = {
    labels: ['고정금리', '변동금리'],
    datasets: [
      {
        label: '최저 금리',
        backgroundColor: '#f87979',
        data: [
          apartmentFixedRate ? apartmentFixedRate.lend_rate_min : 0,
          apartmentVariableRate ? apartmentVariableRate.lend_rate_min : 0
        ]
      },
      {
        label: '최고 금리',
        backgroundColor: '#aad1e6',
        data: [
          apartmentFixedRate ? apartmentFixedRate.lend_rate_max : 0,
          apartmentVariableRate ? apartmentVariableRate.lend_rate_max : 0
        ]
      },
      {
        label: '전월 취급 평균금리',
        backgroundColor: '#82ca9d',
        data: [
          apartmentFixedRate ? apartmentFixedRate.lend_rate_avg : 0,
          apartmentVariableRate ? apartmentVariableRate.lend_rate_avg : 0
        ]
      }
    ]
  }

  // 아파트 외 담보 유형 차트 데이터 업데이트
  const nonApartmentData = loan.value.loanoption_set.filter(option => option.mrtg_type_nm !== '아파트')
  const nonApartmentFixedRate = nonApartmentData.find(option => option.lend_rate_type_nm === '고정금리')
  const nonApartmentVariableRate = nonApartmentData.find(option => option.lend_rate_type_nm === '변동금리')

  nonApartmentChartData.value = {
    labels: ['고정금리', '변동금리'],
    datasets: [
      {
        label: '최저 금리',
        backgroundColor: '#f87979',
        data: [
          nonApartmentFixedRate ? nonApartmentFixedRate.lend_rate_min : 0,
          nonApartmentVariableRate ? nonApartmentVariableRate.lend_rate_min : 0
        ]
      },
      {
        label: '최고 금리',
        backgroundColor: '#aad1e6',
        data: [
          nonApartmentFixedRate ? nonApartmentFixedRate.lend_rate_max : 0,
          nonApartmentVariableRate ? nonApartmentVariableRate.lend_rate_max : 0
        ]
      },
      {
        label: '전월 취급 평균금리',
        backgroundColor: '#82ca9d',
        data: [
          nonApartmentFixedRate ? nonApartmentFixedRate.lend_rate_avg : 0,
          nonApartmentVariableRate ? nonApartmentVariableRate.lend_rate_avg : 0
        ]
      }
    ]
  }
}

// 차트 초기설정
const apartmentChartData = ref({
  labels: ['고정금리', '변동금리'],
  datasets: [
    {
      label: '최저 금리',
      backgroundColor: '#f87979',
      data: [0, 0]
    },
    {
      label: '최고 금리',
      backgroundColor: '#aad1e6',
      data: [0, 0]
    },
    {
      label: '전월 취급 평균금리',
      backgroundColor: '#82ca9d',
      data: [0, 0]
    }
  ]
})

const nonApartmentChartData = ref({
  labels: ['고정금리', '변동금리'],
  datasets: [
    {
      label: '최저 금리',
      backgroundColor: '#f87979',
      data: [0, 0]
    },
    {
      label: '최고 금리',
      backgroundColor: '#aad1e6',
      data: [0, 0]
    },
    {
      label: '전월 취급 평균금리',
      backgroundColor: '#82ca9d',
      data: [0, 0]
    }
  ]
})

// 차트 옵션 설정
const options = {
  responsive: true,
  maintainAspectRatio: true, // 세로 길이를 고정
  aspectRatio: 2, // 세로길이 2로 설정함, 가로는 부모에 따라 조정됨
  scales: {
    x: {
      ticks: {
        autoSkip: false
      }
    }
  },
  plugins: {
    legend: {
      display: true
    }
  },
}

// 가입한 상품 조회
const getContract = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${loanStore.API_URL}/fin_products/loan/contract/${loan.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        loanStore.contractedLoan = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }



// 상품이 계약됐는지 판단
const isContracted = computed(() => {
  if (loanStore.contractedLoan.length === 0) {
    return false
  } 
  const findPrd = loanStore.contractedLoan.findIndex((prd) => prd.fin_prdt_cd === loan.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  return false
})


// 상품 계약
const addContract = (prd) => {
  loanStore.contractedLoan.push(prd)

  axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan/contract/${loan.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: loan.value.fin_prdt_cd
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
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan/contract/${loan.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: loan.value.fin_prdt_cd
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



// 관심상품 조회
const getSave = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${loanStore.API_URL}/fin_products/loan/like/${loan.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        loanStore.savedLoan = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }


// 관심상품 저장하고 있는지 판단
const isSaved = computed(() => {
  if (loanStore.savedLoan.length === 0) {
    return false
  } 
  const findPrd = loanStore.savedLoan.findIndex((prd) => prd.fin_prdt_cd === loan.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  return false
})


// 관심상품 저장
const addSave = (prd) => {
  loanStore.savedLoan.push(prd)

  axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan/like/${loan.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: loan.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        loanStore.savedLoan.push(loan)
      })
      .catch(error => {
        console.log(error)
      })

  }
  

// 관심상품 저장 취소
const delSave = (fin_prdt_cd) => {
  const idx = loanStore.savedLoan.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan/like/${loan.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: loan.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        loanStore.savedLoan.splice(idx, 1) 
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
