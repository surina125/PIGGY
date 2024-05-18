<template>
  <div>
    <h1>적금</h1>

    <!-- 적금 타입 선택 버튼 -->
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
      <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked value="all_type" v-model="selectedType">
      <label class="btn btn-outline-primary" for="btnradio1">전체</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" value="정액적립식" v-model="selectedType">
      <label class="btn btn-outline-primary" for="btnradio2">정기 적금</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off" value="자유적립식" v-model="selectedType">
      <label class="btn btn-outline-primary" for="btnradio3">자유 적금</label>
    </div>

    <!-- 은행 선택 버튼 -->
    <select class="form-select form-select-lg mb-3" aria-label="Large select example" v-model="selectedBank">
      <option class="selected" value="all_bank">전체 은행</option>
      <option 
        v-for="(bank, index) in savingStore.banks"
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
          <th scope="col" @click="sort('6')">6개월 (Click to sort↓)</th>
          <th scope="col" @click="sort('12')">12개월 (Click to sort↓)</th>
          <th scope="col" @click="sort('24')">24개월 (Click to sort↓)</th>
          <th scope="col" @click="sort('36')">36개월 (Click to sort↓)</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(prd, index) in savingStore.savings"
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
import { useSavingStore } from '@/stores/saving.js'
import { useAuthStore } from '@/stores/auth.js'
import { ref, watchEffect, onMounted, computed } from 'vue'
import axios from 'axios'

const savingStore = useSavingStore()
const authStore = useAuthStore()

const selectedBank = ref('all_bank')
const selectedType = ref('all_type')

const fetchData = () => {
  axios.get(`${savingStore.API_URL}/fin_products/saving/${selectedBank.value}/${selectedType.value}/`)
    .then(response => {
      savingStore.savings = response.data
      console.log(`Data fetched from: ${savingStore.API_URL}/fin_products/saving/${selectedBank.value}/${selectedType.value}/`)
    })
    .catch(error => {
      console.error('Error fetching data:', error)
    })
}

watchEffect(() => {
  fetchData()
})

const sort = (num) => {
  axios.get(`${savingStore.API_URL}/fin_products/saving/${selectedBank.value}/${selectedType.value}/sort/${num}/`)
    .then(response => {
      savingStore.savings = response.data
      console.log(num)
      console.log(`${savingStore.API_URL}/fin_products/saving/${selectedBank.value}/${selectedType.value}/sort/${num}/`)
    })
    .catch(error => {
      console.error('Error sorting data:', error)
    })
}

// 특정 저축 기간에 대한 이자율 찾는 함수
const getInterestRate = (prd, term) => {
  if (!prd.savingoption_set) return '-'; // savingoption_set이 정의되지 않은 경우
  const option = prd.savingoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
}


// 모달
const saving = ref({})

const modal_click = function(prd) {
  saving.value = prd
  savingStore.forChartSaving = prd
  console.log(savingStore.forChartSaving)
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
onMounted(() => {
  if (authStore.isAuthenticated && savingStore.contractedSaving.length !== 0 && saving.value) {
    getContract()
  }
})


// 상품이 계약됐는지 판단
const isContracted = computed(() => {
  if (savingStore.contractedSaving.length === 0) {
    return false
  } 
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
onMounted(() => {
  if (authStore.isAuthenticated && savingStore.savedSaving.length !== 0 && saving.value) {
    getSave()
  }
})


// 관심상품 저장하고 있는지 판단
const isSaved = computed(() => {
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
  savingStore.savedSaving.push(prd)

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
        savingStore.savedSaving.push(saving)
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
</style>
