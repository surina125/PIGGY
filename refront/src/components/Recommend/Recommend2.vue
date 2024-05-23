<template>

  <form @submit.prevent="submitForm" class="form-container">
    <div class="question-page">
      <label for="product-type" class="question-label">예금, 적금, 주택담보대출 중에 원하는 상품을 선택하세요:</label>
      <select v-model="selectedProduct" id="product-type" class="form-select form-select-lg mb-4" aria-label="상품 유형 선택">
        <option value="" disabled selected>상품 유형 선택</option>
        <option value="예금">예금</option>
        <option value="적금">적금</option>
        <option value="대출">주택담보대출</option>
      </select>

      <!-- 예금을 선택했을 경우 -->
      <div v-if="selectedProduct === '예금'">
        <label for="period-select" class="question-label">예금의 기간을 선택하세요</label>
        <select v-model="period" id="period-select" class="form-select form-select-lg mb-4" aria-label="기간 선택">
          <option value="" disabled selected>기간 선택</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>

  
        <label for="interest-rate" class="question-label mt-4 mb-5">원하는 최소한의 금리를 입력하세요:</label>
        <div class="slider-container mb-4">
          <span class="range-value">{{ interestRate }}%</span>
          <input type="range" v-model="interestRate" id="interest-rate" min="0" max="10" step="0.1" class="form-range">
        </div>

        <label class="question-label">선호하는 은행을 선택하세요:</label>
        <div class="bank-buttons mb-4">
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
        <label for="type-select" class="question-label">적금유형을 선택하세요</label>
        <select v-model="type" id="type-select" class="form-select form-select-lg mb-4" aria-label="적금 유형">
          <option value="" disabled selected>적금 유형</option>
          <option value="all_type">전체(정기/자유)</option>
          <option value="정액적립식">정기적금</option>
          <option value="자유적립식">자유적금</option>
        </select>

        <label for="period-select" class="question-label">적금의 기간을 선택하세요</label>
        <select v-model="period" id="period-select" class="form-select form-select-lg mb-4" aria-label="기간 선택">
          <option value="" disabled selected>기간 선택</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>

        <label for="interest-rate" class="question-label mt-4 mb-5">원하는 최소한의 금리를 입력하세요:</label>
        <div class="slider-container mb-4">
          <span class="range-value">{{ interestRate }}%</span>
          <input type="range" v-model="interestRate" id="interest-rate" min="0" max="10" step="0.1" class="form-range">
        </div>

        <label class="question-label">선호하는 은행을 선택하세요:</label>
        <div class="bank-buttons mb-4">
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
        <label for="type-select" class="question-label">담보유형을 선택하세요</label>
        <select v-model="type" id="type-select" class="form-select form-select-lg mb-4" aria-label="유형 선택">
          <option value="" disabled selected>담보 유형</option>
          <option value="아파트">아파트</option>
          <option value="아파트외">아파트외</option>
        </select>

        <label class="question-label mt-4">선호하는 금융회사를 선택하세요:</label>
        <div class="bank-buttons mb-4">
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
    </div>

    <button type="submit" class="btn btn-primary mt-4">제출</button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useDepositStore } from '@/stores/deposit'
import { useSavingStore } from '@/stores/saving'
import { useLoanStore } from '@/stores/loan'
import { useRecommendStore } from '@/stores/recommend'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const selectedProduct = ref("")
const period = ref("")
const selectedBanks = ref([])
const type = ref("")
const interestRate = ref(0) 

const depositStore = useDepositStore()
const savingStore = useSavingStore()
const loanStore = useLoanStore()
const recommendStore = useRecommendStore()

watch(selectedProduct, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    selectedBanks.value = []
    period.value = ""
    type.value = ""
    interestRate.value = 0 
  }
  if (newValue === "예금") {
    depositStore.getAll()
  } else if (newValue === "적금") {
    savingStore.getAll()
  } else if (newValue === "주택담보대출") {
    loanStore.loans = []
    loanStore.Aloans = []
    loanStore.Eloans = []
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
  if (selectedProduct.value === '예금') {
    depositStore.getAll();
    const depos = depositStore.deposits;

    const banks = selectedBanks.value.length > 0 ? selectedBanks.value : depositStore.banks;

    let filteredDeposits = depos.filter((deposit) => {
      return (
        banks.includes(deposit.kor_co_nm) &&
        deposit.depositoption_set.some(
          (option) =>
            option.save_trm === period.value && option.intr_rate >= interestRate.value
        )
      );
    });

    if (filteredDeposits.length < 10) {
      let additionalDeposits = depos.filter((deposit) => {
        return deposit.depositoption_set.some(
          (option) => option.save_trm === period.value && option.intr_rate >= interestRate.value
        );
      });

      const uniqueDeposits = new Set(filteredDeposits.map(d => d.id));
      additionalDeposits.forEach(deposit => {
        if (!uniqueDeposits.has(deposit.id) && filteredDeposits.length < 10) {
          filteredDeposits.push(deposit);
          uniqueDeposits.add(deposit.id);
        }
      });
    }

    if (filteredDeposits.length < 10) {
      let additionalDeposits = depos.filter((deposit) => {
        return (
          banks.includes(deposit.kor_co_nm) &&
          deposit.depositoption_set.some(
            (option) => option.save_trm === period.value
          )
        );
      });

      additionalDeposits.sort((a, b) => {
        const aRate = Math.max(...a.depositoption_set.map(option => option.intr_rate));
        const bRate = Math.max(...b.depositoption_set.map(option => option.intr_rate));
        return bRate - aRate;
      });

      const uniqueDeposits = new Set(filteredDeposits.map(d => d.id));
      additionalDeposits.forEach(deposit => {
        if (!uniqueDeposits.has(deposit.id) && filteredDeposits.length < 10) {
          filteredDeposits.push(deposit);
          uniqueDeposits.add(deposit.id);
        }
      });
    }

    if (filteredDeposits.length < 10) {
      let additionalDeposits = depos.filter((deposit) => {
        return deposit.depositoption_set.some(
          (option) => option.save_trm === period.value
        );
      });

      additionalDeposits.sort((a, b) => {
        const aRate = Math.max(...a.depositoption_set.map(option => option.intr_rate));
        const bRate = Math.max(...b.depositoption_set.map(option => option.intr_rate));
        return bRate - aRate;
      });

      const uniqueDeposits = new Set(filteredDeposits.map(d => d.id));
      additionalDeposits.forEach(deposit => {
        if (!uniqueDeposits.has(deposit.id) && filteredDeposits.length < 10) {
          filteredDeposits.push(deposit);
          uniqueDeposits.add(deposit.id);
        }
      });
    }

    recommendStore.deposits = filteredDeposits;
    recommendStore.deposits_period = period.value
    console.log(recommendStore.deposits)
  } else if (selectedProduct.value === '적금') {
    savingStore.getAll();
    const savings = savingStore.savings;

    const banks = selectedBanks.value.length > 0 ? selectedBanks.value : savingStore.banks;

    let filteredSavings = savings.filter((saving) => {
      return (
        banks.includes(saving.kor_co_nm) &&
        saving.savingoption_set.some(
          (option) =>
          (type.value === 'all_type' || option.rsrv_type_nm === type.value) &&
            option.save_trm === period.value &&
            option.intr_rate >= interestRate.value
        )
      );
    });

    if (filteredSavings.length < 10) {
      let additionalSavings = savings.filter((saving) => {
        return saving.savingoption_set.some(
          (option) =>
          (type.value === 'all_type' || option.rsrv_type_nm === type.value) &&
            option.save_trm === period.value &&
            option.intr_rate >= interestRate.value
        );
      });

      const uniqueSavings = new Set(filteredSavings.map(s => s.id));
      additionalSavings.forEach(saving => {
        if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
          filteredSavings.push(saving);
          uniqueSavings.add(saving.id);
        }
      });
    }

    if (filteredSavings.length < 10) {
      let additionalSavings = savings.filter((saving) => {
        return (
          banks.includes(saving.kor_co_nm) &&
          saving.savingoption_set.some(
            (option) =>
            (type.value === 'all_type' || option.rsrv_type_nm === type.value) &&
              option.save_trm === period.value
          )
        );
      });

      additionalSavings.sort((a, b) => {
        const aRate = Math.max(...a.savingoption_set.map(option => option.intr_rate));
        const bRate = Math.max(...b.savingoption_set.map(option => option.intr_rate));
        return bRate - aRate;
      });

      const uniqueSavings = new Set(filteredSavings.map(s => s.id));
      additionalSavings.forEach(saving => {
        if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
          filteredSavings.push(saving);
          uniqueSavings.add(saving.id);
        }
      });
    }

    if (filteredSavings.length < 10) {
      let additionalSavings = savings.filter((saving) => {
        return saving.savingoption_set.some(
          (option) =>
          (type.value === 'all_type' || option.rsrv_type_nm === type.value) &&
            option.save_trm === period.value
        );
      });

      additionalSavings.sort((a, b) => {
        const aRate = Math.max(...a.savingoption_set.map(option => option.intr_rate));
        const bRate = Math.max(...b.savingoption_set.map(option => option.intr_rate));
        return bRate - aRate;
      });

      const uniqueSavings = new Set(filteredSavings.map(s => s.id));
      additionalSavings.forEach(saving => {
        if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
          filteredSavings.push(saving);
          uniqueSavings.add(saving.id);
        }
      });
    }

    recommendStore.savings = filteredSavings;
    console.log(recommendStore.savings);
    recommendStore.savings_type = type.value
    recommendStore.savings_period = period.value

  } else {
    let loans;

    if (type.value === '아파트') {
      loans = loanStore.Aloans
    } else {
      loans = loanStore.Eloans
    }

    const banks = selectedBanks.value.length > 0 ? selectedBanks.value : loanStore.banks

    let filteredLoans = loans.filter((loan) => {
      return banks.includes(loan.kor_co_nm)
    });

    filteredLoans.sort((a, b) => a.lend_rate_min - b.lend_rate_min)
    filteredLoans = filteredLoans.slice(0, 10)

    if (filteredLoans.length < 10) {
      let additionalLoans = loans.filter((loan) => {
        return loan.mrtg_type_nm === type.value
      })

      additionalLoans.sort((a, b) => a.lend_rate_min - b.lend_rate_min)

      const uniqueLoans = new Set(filteredLoans.map(l => l.fin_prdt_cd))
      additionalLoans.forEach(loan => {
        if (!uniqueLoans.has(loan.fin_prdt_cd) && filteredLoans.length < 10) {
          filteredLoans.push(loan)
          uniqueLoans.add(loan.fin_prdt_cd)
        }
      })
    }


    recommendStore.loans = filteredLoans;
    recommendStore.loas_type = type.value;
  }

  alert('폼이 제출되었습니다!')
  router.push({ name: 'deposit2', params: {username: authStore.userData.username} });
}
</script>

<style scoped>
.form-container {
  max-width: 700px;
  margin: auto;
  margin-top: 40px;
  padding: 50px;
  border: 1px solid #ccc;
  border-radius: 15px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 100%;
}

.question-page {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 25px; /* 질문들 사이 간격 조정 */
}

.question-label {
  color: #333333;
  font-size: 1.4em; /* 글자 크기 조정 */
  font-weight: bold; /* 굵게 설정 */
  margin-bottom: 10px;
}

.form-control {
  width: 100%;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1.1em;
}

.form-range {
  width: 100%;
  margin-bottom: 20px;
}

.slider-container {
  position: relative;
  margin-bottom: 50px;
}

.range-value {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  font-weight: bold;
  font-size: 1.4em;
}

.bank-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 15px;
}

.btn.selected {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.btn {
  padding: 12px 20px;
  cursor: pointer;
  font-size: 1.1em;
}

select,
input[type="range"] {
  border-radius: 5px;
}

button[type="submit"] {
  margin-top: 30px;
  background-color: #007bff;
  border: none;
  color: white;
  padding: 12px 30px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.2em;
}

button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>
