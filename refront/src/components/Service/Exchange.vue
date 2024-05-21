 <template>
  <div class="container mt-5">
    <h1 class="text-center">환율 계산기</h1>

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
        <input id="foreign-amount" type="number" class="form-control" v-model="amountForeign" @input="convertToKRW" />
      </div>
      <div class="col-md-6 mb-3">
        <label for="krw-amount" class="form-label">한국 원화 (KRW)</label>
        <input id="krw-amount" type="number" class="form-control" v-model="amountKRW" @input="convertToForeign" />
      </div>
    </div>

    <div v-if="selectedCurrency" class="mt-4">
      <h2>계산 결과</h2>
      <p>한국 원화: {{ formattedKRW }}</p>
      <p>{{ selectedCurrency.cur_unit }}: {{ formattedForeign }}</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';

// State variables
const exchange_infos = ref([]);
const selectedCurrency = ref(null);
const amountKRW = ref(0);
const amountForeign = ref(0);

// Fetch exchange rates on component mount
onMounted(() => {
  fetchExchangeRates();
});

const fetchExchangeRates = () => {
  axios.get("http://127.0.0.1:8000/exchange/exchange_info/")
    .then(response => {
      exchange_infos.value = response.data;
    })
    .catch(error => {
      console.error(error);
    });
};

const convertToForeign = () => {
  if (selectedCurrency.value) {
    const ttsWithoutComma = selectedCurrency.value.tts.replace(/,/g, "");
    amountForeign.value = (amountKRW.value / parseFloat(ttsWithoutComma)).toFixed(2);
  }
};

const convertToKRW = () => {
  if (selectedCurrency.value) {
    const ttbWithoutComma = selectedCurrency.value.ttb.replace(/,/g, "");
    amountKRW.value = (amountForeign.value * parseFloat(ttbWithoutComma)).toFixed(2);
  }
};

// Computed properties for formatted results
const formattedKRW = computed(() => parseFloat(amountKRW.value).toLocaleString());
const formattedForeign = computed(() => parseFloat(amountForeign.value).toLocaleString());
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
</style>
