<template>
  <div>
    <h1>주택담보대출</h1>

    <!-- 대출 타입 선택 버튼 -->
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
      <!-- <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked value="all_type" v-model="selectedType">
      <label class="btn btn-outline-primary" for="btnradio1">전체</label> -->

      <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" value="아파트" v-model="selectedType" selected>
      <label class="btn btn-outline-primary" for="btnradio2">아파트</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off" value="아파트외" v-model="selectedType">
      <label class="btn btn-outline-primary" for="btnradio3">아파트외</label>
    </div>

    <!-- 은행 선택 버튼 -->
    <select class="form-select form-select-lg mb-3" aria-label="Large select example" v-model="selectedBank">
      <option class="selected" value="all_bank">전체 은행</option>
      <option 
        v-for="(bank, index) in loanStore.banks"
        :key="index"
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
          <th scope="col">담보유형</th>
          <th scope="col">대출금리유형</th>
          <th scope="col" @click="sort('min')">최저 대출금리</th>
          <th scope="col" @click="sort('max')">최고 대출금리 </th>
          <th scope="col" @click="sort('avg')">전월 취급 평균금리 </th>
        </tr>
      </thead>

      <!-- 담보유형 아파트인 경우 -->
      <!-- <tbody v-if="selectedType === '아파트'"> -->
      <tbody>
        <tr 
          v-for="(prd, index) in loanStore.selectedLoans"
          :key="index"
          data-bs-toggle="modal" data-bs-target="#exampleModal"
          @click="modal_click(prd)"
        >
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ prd.dcls_month }}</td>
          <td>{{ prd.kor_co_nm }}</td>
          <td>{{ prd.fin_prdt_nm }}</td>
          <td>{{ prd.mrtg_type_nm }}</td>
          <td>{{ prd.lend_rate_type_nm }}</td>
          <td>{{ prd.lend_rate_min }}</td>
          <td>{{ prd.lend_rate_max }}</td>
          <td v-if="prd.lend_rate_avg">{{ prd.lend_rate_avg }}</td>
          <td v-else>-</td>
        </tr>
      </tbody>
      <!-- 담보유형 아파트외인 경우 -->
      <!-- <tbody v-if="selectedType === '아파트외'">
        <tr 
          v-for="(prd, index) in loanStore.Eloans"
          :key="index"
          data-bs-toggle="modal" data-bs-target="#exampleModal"
          @click="modal_click(prd)"
        >
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ prd.dcls_month }}</td>
          <td>{{ prd.kor_co_nm }}</td> -->
          <!-- 상품명 찍히는 것도 있고 안찍히는 것도 있음(확인필요) -->
          <!-- <td v-if="prd.fin_prdt_nm">{{ prd.fin_prdt_nm }}</td>
          <td v-else>-</td>
          <td>{{ prd.mrtg_type_nm }}</td>
          <td>{{ prd.lend_rate_type_nm }}</td>
          <td>{{ prd.lend_rate_min }}</td>
          <td>{{ prd.lend_rate_max }}</td>
          <td>{{ prd.lend_rate_avg }}</td>
        </tr>
      </tbody> -->
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
                  <td>{{ loan.mrtg_type_nm }}</td>
                </tr>
                <tr>
                  <th scope="row">대출금리유형</th>
                  <td>{{ loan.lend_rate_type_nm }}</td>
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
                  <!-- 차트 -->
                  <td v-if="loan" colspan="7">
                    <Bar class="chart-page" :data="chartData" :options="options"/>
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
import { ref, watchEffect, onMounted, computed } from 'vue'
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

onMounted(() => {
  loanStore.getAll()
})

console.log(loanStore.Aloans)

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

// 기간별로 저축금리 가져오기
// const getInterestRate = (prd, term) => {
//   if (!prd || !prd.loanoption_set) return '-';

//   const option = prd.loanoption_set.find(option => option.save_trm === term);
//   return option ? option.intr_rate : '-';
// }

// // 기간별로 최고 우대금리 가져오기
// const getInterestRate2 = (prd, term) => {
//   if (!prd || !prd.loanoption_set) return '-';

//   const option = prd.loanoption_set.find(option => option.save_trm === term);
//   return option ? option.intr_rate2 : '-';
// }

const selectedBank = ref('all_bank')
const selectedType = ref('아파트')

// selectedBank와 selectedType 값이 변경될 때마다 데이터 갱신
const updateSelectedLoans = () => {
  if (selectedBank.value === 'all_bank') {
    if (selectedType.value === '아파트') {
      loanStore.selectedLoans = loanStore.Aloans;
    } else {
      loanStore.selectedLoans = loanStore.Eloans;
    }
  } else {
    if (selectedType.value === '아파트') {
      loanStore.selectedLoans = loanStore.Aloans.filter(loan => loan.kor_co_nm === selectedBank.value);
    } else {
      loanStore.selectedLoans = loanStore.Eloans.filter(loan => loan.kor_co_nm === selectedBank.value);
    }
  }
  console.log(loanStore.selectedLoans);
};

// selectedBank와 selectedType의 변화를 감지하여 updateSelectedLoans 호출
watchEffect(() => {
  updateSelectedLoans();
});


// function updateSelectedLoans() {
//   if (newValue === 'all_bank') {
//     if (selectedType === '아파트') {
//       loanStore.selectedLoans = loanStore.Aloans
//     } else {
//       loanStore.selectedLoans = loanStore.Eloans
//     }
//   } else {
//     if (selectedType === '아파트') {
//       loanStore.selectedLoans = loanStore.Aloans.filter(loan => loan.kor_co_nm === selectedBank.value)
//     } else {
//       loanStore.selectedLoans = loanStore.Eloans.filter(loan => loan.kor_co_nm === selectedBank.value)
//     }
//   }
// }

// watch(obj, prop, callback) {
//   let value = obj[prop];

//   Object.defineProperty(obj, prop, {
//     get() {
//       return value;
//     },
//     set(newValue) {
//       value = newValue;
//       callback(newValue);
//     },
//     configurable: true
//   });
// }

// // watch 설정
// watch(window, 'selectedBank', updateSelectedLoans);
// watch(window, 'selectedType', updateSelectedLoans);

// watch 함수 구현
// function watch(property, callback) {
//   let currentValue = property;
//   Object.defineProperty(window, property, {
//     get() {
//       return currentValue;
//     },
//     set(newValue) {
//       currentValue = newValue;
//       callback(newValue);
//     }
//   });
// }

// // selectedBank와 selectedType의 변화를 감지하여 처리
// watch('selectedBank', (newValue) => {
//   updateSelectedLoans();
// });

// watch('selectedType', (newValue) => {
//   updateSelectedLoans();
// });

// const fetchData = () => {
//   console.log(`${loanStore.API_URL}/fin_products/loan/${selectedBank.value}/${selectedType.value}/`)
//   axios.get(`${loanStore.API_URL}/fin_products/loan/${selectedBank.value}/${selectedType.value}/`)
//     .then(response => {
//       loanStore.loans = response.data
//       console.log(response.data)
      
//     })
//     .catch(error => {
//       console.log(error)
//     })
// }

// watchEffect(() => {
//   fetchData()
// })

// const sort = (num) => {
//   axios.get(`${loanStore.API_URL}/fin_products/loan/${selectedBank.value}/${selectedType.value}/sort/${num}/`)
//     .then(response => {
//       loanStore.loans = response.data
//     })
//     .catch(error => {
//       console.log(error)
//     })
// }


// 모달
const loan = ref({})

const modal_click = function(prd) {
  loan.value = prd

  getContract()
  getSave()

  // 모달창 열리면 차트 안에 데이터 갱신
  chartData.value = {
    labels: ['최저 대출금리', '최고 대출금리', '전월 취급 평균금리'],
    datasets: [
      {
        label: '대출 금리',
        backgroundColor: '#f87979',
        data: [
          loan.value.lend_rate_min || 0,
          loan.value.lend_rate_max || 0,
          loan.value.lend_rate_avg || 0,
        ]
      },
    ]
  }
}


// 차트 초기설정
const chartData = ref({
      labels: [
        '최저 대출금리',
        '최고 대출금리',
        '24개월',
        '전월 취급 평균금리',
      ],
      datasets: [
        {
          label: '대출 금리',
          backgroundColor: '#f87979',
          data: [0,0,0]
        },
      ]
    });

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
  barThickness: 80, // 막대의 두께를 10px로 설정
};


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
