<template>
  <div>
    <h1>정기예금</h1>

    <!-- 은행 선택 버튼 -->
    <select class="form-select form-select-lg mb-3" aria-label="Large select example" v-model="selectedBank">
      <option class="selected" value="all">전체 은행</option>
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
          <th scope="col">6개월</th>
          <th scope="col">12개월</th>
          <th scope="col">24개월</th>
          <th scope="col">36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(prd, index) in depositStore.deposits"
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
    <div v-if="deposit" class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-scrollable modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{deposit.fin_prdt_nm}}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            ...
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary">가입 신청</button>
            <button type="button" class="btn btn-primary">가입 취소</button>
            <button type="button" class="btn btn-primary">가입 신청</button>
            <button type="button" class="btn btn-primary">관심상품 저장</button>
          </div>
        </div>
      </div>
    </div>

  </div>


  
</template>

<script setup>
import { useDepositStore } from '@/stores/deposit.js'
import { ref, watch } from 'vue'

const depositStore = useDepositStore()

// 전체 조회
depositStore.getAll()

// 특정 저축 기간에 대한 이자율 찾는 함수
const getInterestRate = (prd, term) => {
  const option = prd.depositoption_set.find(option => option.save_trm === term)
  return option ? option.intr_rate : '-'
}


// 특정 은행 선택 시 조회
const selectedBank = ref('all')

// selectedBank 값이 변경될 때마다 데이터 갱신
watch(selectedBank, (newValue) => {
  if (newValue === 'all') {
    depositStore.getAll()
  } else {
    depositStore.selectBank(selectedBank.value)
  }
})


// 모달
const deposit = ref({})

const model = function(prd) {
  deposit.value = prd
}

</script>


<style scoped>

</style>
