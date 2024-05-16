<template>
  <div>
    <Bar
      :options="chartOptions"
      :data="chartData"
    />
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/users'
import colors from 'vuetify/util/colors'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Colors } from 'chart.js'

const userStore = useUserStore()

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  labels: Array,
  lendRateAvg: Array,
  lendRateMax: Array,
  lendRateMax: Array,
})

const chartData = {
  labels: props.labels,
  datasets: [
    {
      label: '전월 취급 평균 금리',
      data: props.lendRateAvg,
      backgroundColor: colors.grey.base,
      stack: 'Stack 0'
    },
    {
      label: '최저 대출 금리',
      data: props.lendRateMin,
      backgroundColor: '#1089FF',
      stack: 'Stack 1'
    },
    {
      label: '최고 대출 금리',
      data: props.lendRateMax,
      backgroundColor: colors.red.accent2,
      stack: 'Stack 2'
    },
  ]
}

const chartOptions = ref({
  plugins: {
    title: {
      display: true,
      text: `${userStore.userInfo.name}님의 가입한 상품 금리`
    },
  },
  responsive: true,
  scales: {
    x: {
      stacked: true,
      ticks: {
        maxRotation: 30,
        minRotation: 0,
        font: {
          size: 8
        }
      }
    },
  },
})
</script>


<style scoped>

</style>