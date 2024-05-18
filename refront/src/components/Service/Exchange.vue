<template>

  <div>    

    <h1>환율</h1>
    
    <select v-model="selectedCurrency">
      <option v-for="exchange_info in exchange_infos" :key="exchange_info.id" :value="exchange_info">
        {{ exchange_info.cur_unit }}
      </option>
    </select>
  
    <div>
      <h2>환율 계산기</h2>
      <input v-model="amountForeign" @input="convertToKRW" 
             :placeholder="selectedCurrency ? selectedCurrency.cur_unit : '외화'" />
      <input v-model="amountKRW" @input="convertToForeign" placeholder="한국 원화 (KRW)" />
    </div>
    
    <div v-if="selectedCurrency">
      <h2>계산 결과</h2>
      <p>한국 원화: {{ formattedKRW }}</p>
      <p>{{ selectedCurrency.cur_unit }}: {{ formattedForeign }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';


const exchange_infos = ref([]);
const selectedCurrency = ref(null);
const amountKRW = ref(0);
const amountForeign = ref(0);

onMounted(() => {
  fetchExchangeRates();
});

const result = ref([])

const fetchExchangeRates = () => {
  axios.get("http://127.0.0.1:8000/exchange/exchange_info/")
    .then(response => {
      exchange_infos.value = response.data;
      console.log(exchange_infos.value)

    })
    .catch(error => {
      console.error(error);
    });
};

const convertToForeign = () => {
  if (selectedCurrency.value) {
    let ttsWithoutComma = selectedCurrency.value.tts.replace(/,/g, "");
    amountForeign.value = (amountKRW.value * parseFloat(ttsWithoutComma));
  }
}

const convertToKRW = () => {
  if (selectedCurrency.value) {
    let ttbWithoutComma = selectedCurrency.value.ttb.replace(/,/g, "");
    amountKRW.value = (amountForeign.value * parseFloat(ttbWithoutComma)).toFixed(2);
  }
}


</script>

<style scoped>
h1 {
  font-size: 2em;
  margin-bottom: 20px;
}
select, input {
  display: block;
  margin: 10px 0;
  padding: 8px;
  font-size: 1em;
}
div {
  margin-bottom: 20px;
}
</style>

