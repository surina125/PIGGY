<template>
  <div v-if="exchangeInfos">
    <Bar :chart-data="chartData" :options="options"></Bar>
  </div>
</template>

<script setup>
import { defineProps, ref } from 'vue'
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';


ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

// Props 정의
const props = defineProps({
  exchangeInfos: Array
})

if (props.exchangeInfos) {
  const chartData = {
  labels: props.exchangeInfos.map(currency => currency.cur_nm),
  datasets: [
      {
        label: '기준 환율',
        backgroundColor: '#aad1e6',
        data: props.exchangeInfos.map(currency => parseFloat(currency.deal_bas_r.replace(/,/g, '')))
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 2,
    indexAxis: 'y',
    scales: {
      x: {
        beginAtZero: true
      }
    }
  }
}



</script>

<style scoped>
</style>
