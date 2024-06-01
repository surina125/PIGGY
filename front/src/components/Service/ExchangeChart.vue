<template>
  <div class="mt-1">
    <div style="width: 100%; height: 600px; margin: auto;">
      <canvas id="exchangeChart"></canvas>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue'
import {
  Chart,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

// Register the required components
Chart.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend)

const exchange_infos = ref([]);

const fetchExchangeRates = () => {
  return axios.get("http://127.0.0.1:8000/exchange/exchange_info/")
    .then(response => {
      exchange_infos.value = response.data;
      createChart()
    })
    .catch(error => {
      console.error(error)
    })
}

let exchangeChart = null;

onMounted(() => {
  fetchExchangeRates()
})

const createChart = () => {
  if (exchangeChart) {
    exchangeChart.destroy()
  }

  // 데이터를 내림차순으로 정렬
  const sortedInfos = [...exchange_infos.value].sort((a, b) => parseFloat(b.deal_bas_r.replace(/,/g, '')) - parseFloat(a.deal_bas_r.replace(/,/g, '')))

  const ctx = document.getElementById('exchangeChart').getContext('2d')
  const labels = sortedInfos.map(info => info.cur_unit)
  const dealBasRData = sortedInfos.map(info => parseFloat(info.deal_bas_r.replace(/,/g, '')))
  const ttbData = sortedInfos.map(info => parseFloat(info.ttb.replace(/,/g, '')))
  const ttsData = sortedInfos.map(info => parseFloat(info.tts.replace(/,/g, '')))

  exchangeChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '매매기준율',
          data: dealBasRData,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: '송금 받으실 때',
          data: ttbData,
          backgroundColor: 'rgba(192, 75, 192, 0.2)',
          borderColor: 'rgba(192, 75, 192, 1)',
          borderWidth: 1
        },
        {
          label: '송금 보내실 때',
          data: ttsData,
          backgroundColor: 'rgba(192, 192, 75, 0.2)',
          borderColor: 'rgba(192, 192, 75, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      indexAxis: 'y', // 가로 막대그래프
      maintainAspectRatio: false,
      scales: {
        x: {
          beginAtZero: true
        },
        y: {
          ticks: {
            callback: function(value, index, values) {
              return sortedInfos[index].cur_nm
            }
          }
        }
      }
    }
  });
};
</script>

<style scoped>
canvas {
  max-width: 100%;
}
</style>
