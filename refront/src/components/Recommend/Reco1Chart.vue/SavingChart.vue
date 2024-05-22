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
          <th scope="col">6개월</th>
          <th scope="col">12개월</th>
          <th scope="col">24개월</th>
          <th scope="col">36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(prd, index) in recommendStore.reco1S"
          :key="index"
          data-bs-toggle="modal" data-bs-target="#exampleModal"
          @click="modal_click(prd)"
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
    <div v-if="saving" class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{saving.fin_prdt_nm}}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <table class="table table-hover">
              <tbody>
                <tr>
                  <th class="modal_row" scope="row">공시제출일</th>
                  <td>{{ saving.dcls_month }}</td>
                </tr>
                <tr>
                  <th scope="row">금융회사명</th>
                  <td>{{ saving.kor_co_nm }}</td>
                </tr>
                <!-- <tr>
                  <th scope="row">적립유형</th>
                  <td>{{ saving.savingoption_set[0].rsrv_type_nm }}</td>
                </tr> -->
                <tr>
                  <th scope="row">가입방법</th>
                  <td>{{ saving.join_way }}</td>
                </tr>
                <tr>
                  <th scope="row">가입대상</th>
                  <td>{{ saving.join_member }}</td>
                </tr>
                <tr>
                  <th scope="row">최고 한도</th>
                  <td>{{ saving.max_limit }}</td>
                </tr>
                <tr>
                  <th scope="row">만기 후 이자율</th>
                  <td>{{ saving.mtrt_int }}</td>
                </tr>
                <tr>
                  <th scope="row">우대조건</th>
                  <td>{{ saving.spcl_cnd }}</td>
                </tr>
                <tr>
                  <th scope="row">기타 유의사항</th>
                  <td>{{ saving.etc_note }}</td>
                </tr>
                <tr>
                  <!-- 차트 -->
                  <td v-if="saving" colspan="7">
                    <Bar class="chart-page" :data="chartData" :options="options"/>
                  </td>                  
                </tr>
              </tbody>
            </table>


          </div>

          <!-- 가입신청 / 관심상품 저장 버튼 -->
          <div v-if="authStore.isAuthenticated" class="modal-footer no-border">
            <button type="button" class="btn btn-danger" v-if="isContracted" @click="delContract(saving.fin_prdt_cd)">
              가입 취소
            </button>
            <button type="button" class="btn btn-primary" v-else @click="addContract(saving)">
              가입 신청
            </button>

            <button type="button" class="btn btn-danger" v-if="isSaved" @click="delSave(saving.fin_prdt_cd)">
              저장 취소
            </button>
            <button type="button" class="btn btn-primary" v-else @click="addSave(saving)">
              관심상품 저장
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
  
</template>

<script setup>
import { useSavingStore } from '@/stores/saving'
import { useAuthStore } from '@/stores/auth'
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

const recommendStore = useRecommendStore()

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

// 기간별로 저축금리 가져오기
const getInterestRate = (prd, term) => {
  if (!prd || !prd.savingoption_set) return '-';

  const option = prd.savingoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
}

// 기간별로 최고 우대금리 가져오기
const getInterestRate2 = (prd, term) => {
  if (!prd || !prd.savingoption_set) return '-';

  const option = prd.savingoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate2 : '-';
}

const savingStore = useSavingStore()
const authStore = useAuthStore()


// 모달
const saving = ref({})

const modal_click = function(prd) {
  saving.value = prd

  getContract()
  getSave()

  // 모달창 열리면 차트 안에 데이터 갱신
  chartData.value = {
    labels: ['6개월', '12개월', '24개월', '36개월'],
    datasets: [
      {
        label: '저축 금리',
        backgroundColor: '#f87979',
        data: [
          parseFloat(getInterestRate(saving.value, '6')) || 0,
          parseFloat(getInterestRate(saving.value, '12')) || 0,
          parseFloat(getInterestRate(saving.value, '24')) || 0,
          parseFloat(getInterestRate(saving.value, '36')) || 0
        ]
      },
      {
        label: '최고 우대 금리',
        backgroundColor: '#aad1e6',
        data: [
          parseFloat(getInterestRate2(saving.value, '6')) || 0,
          parseFloat(getInterestRate2(saving.value, '12')) || 0,
          parseFloat(getInterestRate2(saving.value, '24')) || 0,
          parseFloat(getInterestRate2(saving.value, '36')) || 0
        ]
      }
    ]
  }
}


// 차트 초기설정
const chartData = ref({
      labels: [
        '6개월',
        '12개월',
        '24개월',
        '36개월',
      ],
      datasets: [
        {
          label: '저축 금리',
          backgroundColor: '#f87979',
          data: [0,0,0,0]
        },
        {
          label: '최고 우대 금리',
          backgroundColor: '#aad1e6',
          data: [0,0,0,0]
        },
      ]
    });

    // 차트 옵션 설정
    const options = {
      responsive: true,
      maintainAspectRatio: true, // 세로 길이를 고정
      aspectRatio: 2, // 세로길이 2로 설정함, 가로는 부모에 따라 조정됨
    }


// 가입한 상품 조회
const getContract = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${savingStore.API_URL}/fin_products/saving/contract/${saving.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        savingStore.contractedSaving = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }


// 상품이 계약됐는지 판단
const isContracted = computed(() => {
  console.log(savingStore.contractedSaving)
  if (savingStore.contractedSaving.length === 0) {
    return false
  } 
  // console.log(savingStore.contractedSaving)
  const findPrd = savingStore.contractedSaving.findIndex((prd) => prd.fin_prdt_cd === saving.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  return false
})


// 상품 계약
const addContract = (prd) => {
  savingStore.contractedSaving.push(prd)

  axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving/contract/${saving.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: saving.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        savingStore.contractedSaving.push(saving)
      })
      .catch(error => {
        console.log(error)
      })

  }
  

// 상품 계약 취소
const delContract = (fin_prdt_cd) => {
  const idx = savingStore.contractedSaving.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving/contract/${saving.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: saving.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        savingStore.contractedSaving.splice(idx, 1) 
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
      url: `${savingStore.API_URL}/fin_products/saving/like/${saving.value.fin_prdt_cd}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        savingStore.savedSaving = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }


// 관심상품 저장하고 있는지 판단
const isSaved = computed(() => {
  // console.log(123)
  // console.log(savingStore.savedSaving)
  if (savingStore.savedSaving.length === 0) {
    return false
  } 
  const findPrd = savingStore.savedSaving.findIndex((prd) => prd.fin_prdt_cd === saving.value.fin_prdt_cd)
  if (findPrd !== -1) {
    return true
  }
  return false
})


// 관심상품 저장
const addSave = (prd) => {
  // savingStore.savedSaving.push(prd)

  axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving/like/${saving.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: saving.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        savingStore.savedSaving.push(prd)
      })
      .catch(error => {
        console.log(error)
      })

  }
  

// 관심상품 저장 취소
const delSave = (fin_prdt_cd) => {
  const idx = savingStore.savedSaving.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {

    axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving/like/${saving.value.fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: saving.value.fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        savingStore.savedSaving.splice(idx, 1) 
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
/* .chart-page {
  width: 100%;
  height: 30px;
} */
</style>
