<template>
  <div>
    <h1>적금</h1>

    <!-- 적금 타입 선택 버튼 -->
    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
      <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked value="all" v-model="savingType">
      <label class="btn btn-outline-primary" for="btnradio1">전체</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" value="setted" v-model="savingType">
      <label class="btn btn-outline-primary" for="btnradio2">정기 적금</label>

      <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off" value="free" v-model="savingType">
      <label class="btn btn-outline-primary" for="btnradio3">자유 적금</label>
    </div>

    <!-- 은행 선택 버튼 -->
    <select class="form-select form-select-lg mb-3" aria-label="Large select example" v-model="selectedBank">
      <option class="selected" value="all">전체 은행</option>
      <option 
        v-for="bank in savingStore.banks"
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
          <th scope="col">6개월 (Click to sort↓)</th>
          <th scope="col">12개월 (Click to sort↓)</th>
          <th scope="col">24개월 (Click to sort↓)</th>
          <th scope="col">36개월 (Click to sort↓)</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(prd, index) in savingStore.savings"
          :key="prd.id"
          data-bs-toggle="modal" data-bs-target="#exampleModal"
          @click="model(prd)"
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
            {{ saving }}
          </div>

          <!-- 가입신청 / 관심상품 저장 버튼 -->
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" v-if="isContracted" @click="delContract(saving.fin_prdt_cd)">
              가입 취소
            </button>
            <button type="button" class="btn btn-danger" v-else @click="addContract(saving)">
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
import { useSavingStore } from '@/stores/saving.js'
import { useAuthStore } from '@/stores/auth.js'
import { ref, watch, computed, onMounted, watchEffect } from 'vue'
import axios from 'axios'


const savingStore = useSavingStore()
const authStore = useAuthStore()
const savingType = ref('all')

// 전체 조회
savingStore.getAll()

// 특정 저축 기간에 대한 이자율 찾는 함수
const getInterestRate = (prd, term) => {
  const option = prd.savingoption_set.find(option => option.save_trm === term)
  return option ? option.intr_rate : '-'
}


// 특정 은행 선택 시 조회
const selectedBank = ref('all')

// selectedBank 값이 변경될 때마다 데이터 갱신
watch(selectedBank, (newValue) => {
  if (newValue === 'all') {
    savingStore.getAll()
  } else {
    savingStore.selectBank(selectedBank.value)
  }
})





// 모달
const saving = ref({})

const model = function(prd) {
  saving.value = prd
}


// 가입한 상품 조회
const getContract = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${savingStore.API_URL}/fin_products/saving_contract/${saving.value.fin_prdt_cd}/`
    })
      .then(response => {
        savingStore.contractedSaving.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }
onMounted(() => {
  if (savingStore.contractedSaving.length !== 0) {
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
  console.log(savingStore.contractedSaving)
  return false
})


// 상품 계약
const addContract = (prd) => {
  savingStore.contractedSaving.push(prd)

  axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving_contract/${saving.value.fin_prdt_cd}/`,
      data: {
        code: saving.value.fin_prdt_cd
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
      url: `${savingStore.API_URL}/fin_products/saving_contract/${saving.value.fin_prdt_cd}/`,
      data: {
        code: saving.value.fin_prdt_cd
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


</script>


<style scoped>

</style>
