<template>
  <div class="container">

    <div class="mb-3">
      <label for="currency-standard-select" class="form-label">환율 기준</label>
      <select id="currency-standard-select" class="form-select" v-model="selectedStandardCurrency">
        <option value="deal_bas_r">매매기준율</option>
        <option value="ttb">송금 받으실 때</option>
        <option value="tts">송금 보내실 때</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="currency-select" class="form-label">환율 선택</label>
      <select id="currency-select" class="form-select" v-model="selectedCurrency">
        <option v-for="exchange_info in exchange_infos" :key="exchange_info.id" :value="exchange_info">
          {{ exchange_info.cur_unit }}
        </option>
      </select>
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <label for="foreign-amount" class="form-label">{{ selectedCurrency ? selectedCurrency.cur_unit : '외화' }}</label>
        <input id="foreign-amount" type="number" class="form-control fw-bold" v-model="amountForeign" @input="convertToKRW" />
      </div>
      <div class="col-md-6 mb-3">
        <label for="krw-amount" class="form-label">한국 원화 (KRW)</label>
        <input id="krw-amount" type="number" class="form-control fw-bold" v-model="amountKRW" @input="convertToForeign" />
      </div>
    </div>

    <!-- 그래프 -->
    <ExchangeChart/>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import ExchangeChart from './ExchangeChart.vue';

// State variables
const exchange_infos = ref([]);
const selectedCurrency = ref(null);
const amountKRW = ref(0);
const amountForeign = ref(0);
const selectedStandardCurrency = ref('deal_bas_r');

// Fetch exchange rates on component mount
onMounted(() => {
  fetchExchangeRates();
});

const fetchExchangeRates = () => {
  return axios.get("http://127.0.0.1:8000/exchange/exchange_info/")
    .then(response => {
      exchange_infos.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });
};

// 원화 > 외화 (환율기준에 따라)
const convertToForeign = () => {
  if (selectedCurrency.value && selectedStandardCurrency.value) {
    const WithoutComma = selectedCurrency.value[selectedStandardCurrency.value].replace(/,/g, "");
    amountForeign.value = (amountKRW.value / parseFloat(WithoutComma)).toFixed(2);
  }
};

// 외화 > 원화 (환율기준에 따라)
const convertToKRW = () => {
  if (selectedCurrency.value && selectedStandardCurrency.value) {
    const WithoutComma = selectedCurrency.value[selectedStandardCurrency.value].replace(/,/g, "");
    amountKRW.value = (amountForeign.value * parseFloat(WithoutComma)).toFixed(2);
  }
};
</script>

<style scoped>
h1 {
  font-size: 2.5em;
  color: #333;
}

label {
  font-size: 1.2em;
  color: #555;
}

select, input {
  display: block;
  width: 100%;
  padding: 12px;
  font-size: 1.1em;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-shadow: none;
}

input:focus, select:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.1);
}

.container {
  padding: 20px;
}

.row {
  margin-top: 20px;
}
</style>
