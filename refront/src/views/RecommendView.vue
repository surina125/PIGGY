<template>
  <form @submit.prevent="submitForm" class="form-container">
    <div class="question-page">
      <label for="product-type">예금, 적금, 주택담보대출 중에 원하는 상품을 선택하세요:</label>
      <select v-model="selectedProduct" id="product-type" class="form-select form-select-lg mb-3" aria-label="상품 유형 선택">
        <option value="" disabled selected>상품 유형 선택</option>
        <option value="예금">예금</option>
        <option value="적금">적금</option>
        <option value="대출">주택담보대출</option>
      </select>

      <!-- 예금을 선택했을 경우 -->
      <div v-if="selectedProduct === '예금'">
        <label for="period-select">예금의 기간을 선택하세요</label>
        <select v-model="period" id="period-select" class="form-select form-select-lg mb-3" aria-label="기간 선택">
          <option value="" disabled selected>기간 선택</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>

        <label>선호하는 은행을 선택하세요:</label>
        <div class="bank-buttons">
          <button
            v-for="bank in depositStore.banks"
            :key="bank"
            @click="toggleBank(bank)"
            :class="{'selected': selectedBanks.includes(bank)}"
            class="btn btn-outline-primary"
            type="button"
          >
            {{ bank }}
          </button>
        </div>
      </div>

      <!-- 적금을 선택했을 경우 -->
      <div v-if="selectedProduct === '적금'">
        <label for="type-select">적금유형을 선택하세요</label>
        <select v-model="type" id="type-select" class="form-select form-select-lg mb-3" aria-label="적금 유형">
          <option value="" disabled selected>적금 유형</option>
          <option value="all_type">전체(정기/자유)</option>
          <option value="정액적립식">정기적금</option>
          <option value="자유적립식">자유적금</option>
        </select>

        <label for="period-select">예금의 기간을 선택하세요</label>
        <select v-model="period" id="period-select" class="form-select form-select-lg mb-3" aria-label="기간 선택">
          <option value="" disabled selected>기간 선택</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>

        <label>선호하는 은행을 선택하세요:</label>
        <div class="bank-buttons">
          <button
            v-for="bank in savingStore.banks"
            :key="bank"
            @click="toggleBank(bank)"
            :class="{'selected': selectedBanks.includes(bank)}"
            class="btn btn-outline-primary"
            type="button"
          >
            {{ bank }}
          </button>
        </div>
      </div>

      <!-- 대출을 선택했을 경우 -->
      <div v-if="selectedProduct === '대출'">
        <label for="type-select">담보유형을 선택하세요</label>
        <select v-model="type" id="type-select" class="form-select form-select-lg mb-3" aria-label="유형 선택">
          <option value="" disabled selected>담보 유형</option>
          <option value="아파트">아파트</option>
          <option value="아파트외">아파트외</option>
        </select>

        <label>선호하는 금융회사을 선택하세요:</label>
        <div class="bank-buttons">
          <button
            v-for="bank in loanStore.banks"
            :key="bank"
            @click="toggleBank(bank)"
            :class="{'selected': selectedBanks.includes(bank)}"
            class="btn btn-outline-primary"
            type="button"
          >
            {{ bank }}
          </button>
        </div>
      </div>

      <div v-if="selectedProduct === '주택담보대출'">
        <p>대출의 목적을 입력하세요</p>
        <input type="text" v-model="Dpurpose" class="form-control mb-3" />
      </div>
    </div>

    <button type="submit" class="btn btn-primary">제출</button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useDepositStore } from '@/stores/deposit'
import { useSavingStore } from '@/stores/saving'
import { useLoanStore } from '@/stores/loan'

const selectedProduct = ref("")
const period = ref("")
const selectedBanks = ref([])
const type = ref("")

const depositStore = useDepositStore()
const savingStore = useSavingStore()
const loanStore = useLoanStore()

watch(selectedProduct, (newValue, oldValue) => {
  // 상품 유형을 다시 선택했을 때 기간이랑 은행은 비워져야 함
  if (newValue !== oldValue) {
    selectedBanks.value = []
    period.value = ""
    type.value = ""
  }
  if (newValue === "예금") {
    depositStore.getAll()
  } else if (newValue === "적금") {
    savingStore.getAll()
  } else if (newValue === "주택담보대출") {
    loanStore.getAll()
  }
})

const toggleBank = (bank) => {
  if (selectedBanks.value.includes(bank)) {
    selectedBanks.value = selectedBanks.value.filter(b => b !== bank)
  } else {
    selectedBanks.value.push(bank)
  }
}

const submitForm = () => {
  if (selectedProduct.value === "예금") {

  } else if (selectedProduct.value === "적금") {

  } else if (selectedProduct.value === "대출") {
    
  }
  console.log("선호하는 은행들:", selectedBanks.value)
  alert('폼이 제출되었습니다!')
}
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.question-page {
  width: 100%;
  height: 700px;
  display: flex;
  flex-direction: column;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.bank-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.btn.selected {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.btn {
  padding: 10px;
  cursor: pointer;
}
</style>
