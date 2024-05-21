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

        <label for="interest-rate">원하는 최소한의 금리를 입력하세요:</label>
        <div class="slider-container">
          <span class="range-value">{{ interestRate }}%</span>
          <input type="range" v-model="interestRate" id="interest-rate" min="0" max="10" step="0.1" class="form-range">
        </div>

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

        <label for="interest-rate">원하는 최소한의 금리를 입력하세요:</label>
        <div class="slider-container">
          <span class="range-value">{{ interestRate }}%</span>
          <input type="range" v-model="interestRate" id="interest-rate" min="0" max="10" step="0.1" class="form-range">
        </div>

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
       <!-- 대출을 선택했을 경우 -->
       <div v-if="selectedProduct === '대출'">
        <label for="type-select">담보유형을 선택하세요</label>
        <select v-model="type" id="type-select" class="form-select form-select-lg mb-3" aria-label="유형 선택">
          <option value="" disabled selected>담보 유형</option>
          <option value="아파트">아파트</option>
          <option value="아파트외">아파트외</option>
        </select>

        <label>선호하는 금융회사를 선택하세요:</label>
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
    </div>

    <button type="submit" class="btn btn-primary">제출</button>
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
  // 상품 유형을 다시 선택했을 때 기간이랑 은행은 비워져야 함
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


// 폼 제출
const formData = ref({})

const submitForm = () => {
  // 예금 선택 결과
  if (selectedProduct.value === '예금') {
    depositStore.getAll();
    const depos = depositStore.deposits;

    // 선호 은행이 선택되지 않았을 경우 모든 은행을 포함하도록 설정
    const banks = selectedBanks.value.length > 0 ? selectedBanks.value : depositStore.banks;

    // 1. 기간, 최소 금리, 선호 은행 고려
    let filteredDeposits = depos.filter((deposit) => {
      return (
        banks.includes(deposit.kor_co_nm) &&
        deposit.depositoption_set.some(
          (option) =>
            option.save_trm === period.value && option.intr_rate >= interestRate.value
        )
      );
    });

    // 2. 1번째 방법의 결과가 10개 이하이면 기간, 최소 금리 고려해서 높은 것 10개 추가한다. 10개 없으면 그 이하의 개수 추가
    if (filteredDeposits.length < 10) {
      let additionalDeposits = depos.filter((deposit) => {
        return deposit.depositoption_set.some(
          (option) => option.save_trm === period.value && option.intr_rate >= interestRate.value
        );
      });

      // 1의 결과와 중복 제거
      const uniqueDeposits = new Set(filteredDeposits.map(d => d.id));
      additionalDeposits.forEach(deposit => {
        if (!uniqueDeposits.has(deposit.id) && filteredDeposits.length < 10) {
          filteredDeposits.push(deposit);
          uniqueDeposits.add(deposit.id);
        }
      });
    }

    // 3. 2까지의 결과도 10개 이하이면 기간, 은행 가지고 금리가 높은 10개를 추가한다.
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

      // (1+2)의 결과와 중복 제거
      const uniqueDeposits = new Set(filteredDeposits.map(d => d.id));
      additionalDeposits.forEach(deposit => {
        if (!uniqueDeposits.has(deposit.id) && filteredDeposits.length < 10) {
          filteredDeposits.push(deposit);
          uniqueDeposits.add(deposit.id);
        }
      });
    }

    // 4. 최종 단계에서도 결과가 10개 이하이면 기간만 가지고 금리 높은 순으로 10개 추가
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

      // 중복 제거
      const uniqueDeposits = new Set(filteredDeposits.map(d => d.id));
      additionalDeposits.forEach(deposit => {
        if (!uniqueDeposits.has(deposit.id) && filteredDeposits.length < 10) {
          filteredDeposits.push(deposit);
          uniqueDeposits.add(deposit.id);
        }
      });
    }

    // recommendStore에 deposits배열 안에다가 추천받은 예금목록들을 저장
    recommendStore.deposits = filteredDeposits;
    recommendStore.deposits_period = period.value
    console.log(recommendStore.deposits)


  } else if (selectedProduct.value === '적금') {
      // 적금을 선택
      savingStore.getAll();
      const savings = savingStore.savings;

      // 선호 은행이 선택되지 않았을 경우 모든 은행을 포함하도록 설정
      const banks = selectedBanks.value.length > 0 ? selectedBanks.value : savingStore.banks;

      // 1. 상품유형, 기간, 최소 금리, 선호 은행 고려
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

      // 2. 1번째 방법의 결과가 10개 이하이면 상품 유형, 기간, 최소 금리 고려해서 높은 것 10개 추가한다. 10개 없으면 그 이하의 개수 추가
      if (filteredSavings.length < 10) {
        let additionalSavings = savings.filter((saving) => {
          return saving.savingoption_set.some(
            (option) =>
            (type.value === 'all_type' || option.rsrv_type_nm === type.value) &&
              option.save_trm === period.value &&
              option.intr_rate >= interestRate.value
          );
        });

        // 1의 결과와 중복 제거
        const uniqueSavings = new Set(filteredSavings.map(s => s.id));
        additionalSavings.forEach(saving => {
          if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
            filteredSavings.push(saving);
            uniqueSavings.add(saving.id);
          }
        });
      }

      // 3. 2까지의 결과도 10개 이하이면 상품유형, 기간, 은행 가지고 금리가 높은 10개를 추가한다.
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

        // (1+2)의 결과와 중복 제거
        const uniqueSavings = new Set(filteredSavings.map(s => s.id));
        additionalSavings.forEach(saving => {
          if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
            filteredSavings.push(saving);
            uniqueSavings.add(saving.id);
          }
        });
      }

      // 4. 최종 단계에서도 결과가 10개 이하이면 상품유형, 기간만 가지고 금리 높은 순으로 10개 추가
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

        // 중복 제거
        const uniqueSavings = new Set(filteredSavings.map(s => s.id));
        additionalSavings.forEach(saving => {
          if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
            filteredSavings.push(saving);
            uniqueSavings.add(saving.id);
          }
        });
      }

      // 5. 마지막 단계에서도 결과가 10개 이하이면 적금 유형, 기간을 고려하여 금리 높은 순으로 10개 추가
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

        // 중복 제거
        const uniqueSavings = new Set(filteredSavings.map(s => s.id));
        additionalSavings.forEach(saving => {
          if (!uniqueSavings.has(saving.id) && filteredSavings.length < 10) {
            filteredSavings.push(saving);
            uniqueSavings.add(saving.id);
          }
        });
      }

      // recommendStore에 savings 배열 안에다가 추천받은 적금 목록들을 저장
      recommendStore.savings = filteredSavings;
      console.log(recommendStore.savings);
      // 적립유형만 따로 저장해줌
      recommendStore.savings_type = type.value
      recommendStore.savings_period = period.value

      router.push({name: 'recommend'})  

      console.log("Form Data:", formData)
      alert('폼이 제출되었습니다!')
} else {
    // 대출을 선택
    loanStore.getAll();

    let loans; // 여기서 loans 변수를 선언합니다.

    if (type.value === '아파트') {
      loans = loanStore.Aloans;
    } else {
      loans = loanStore.Eloans;
    }

    // 선호 은행이 선택되지 않았을 경우 모든 은행을 포함하도록 설정
    const banks = selectedBanks.value.length > 0 ? selectedBanks.value : loanStore.banks;

    // 1. 은행과 담보 유형을 고려하여 필터링
    let filteredLoans = loans.filter((loan) => {
      return banks.includes(loan.kor_co_nm) && loan.mrtg_type_nm === type.value;
    });


    // 금리가 낮은 순으로 정렬하고 상위 10개 선택
    filteredLoans.sort((a, b) => a.lend_rate_avg - b.lend_rate_avg);
    filteredLoans = filteredLoans.slice(0, 10);

    // 2. 1번째 방법의 결과가 10개 이하이면 담보 유형과 금리를 고려해서 낮은 것 10개 추가
    if (filteredLoans.length < 10) {
      let additionalLoans = loans.filter((loan) => {
        return loan.mrtg_type_nm === type.value;
      });

      // 금리가 낮은 순으로 정렬
      additionalLoans.sort((a, b) => a.lend_rate_avg - b.lend_rate_avg);

      // 중복 제거 후 추가
      const uniqueLoans = new Set(filteredLoans.map(l => l.fin_prdt_cd));
      additionalLoans.forEach(loan => {
        if (!uniqueLoans.has(loan.fin_prdt_cd) && filteredLoans.length < 10) {
          filteredLoans.push(loan);
          uniqueLoans.add(loan.fin_prdt_cd);
        }
      });
    }

    // 필터링된 대출 정보를 recommendStore.loans에 저장
    recommendStore.loas = filteredLoans;
    
  }
  console.log(recommendStore.loas)
  router.push({ name: 'deposit2', params: {username: authStore.userData.username} });
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

.form-range {
  width: 100%;
  margin-bottom: 10px;
}

.slider-container {
  position: relative;
  margin-bottom: 40px;
}

.range-value {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  font-weight: bold;
  font-size: 1.2em;
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
