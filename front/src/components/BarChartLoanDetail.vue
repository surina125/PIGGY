<template>
  <div>
    <Bar
      class="mx-auto"
      style="width: 100%;"
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
  title: String,
  averageIntrRate: Array,
  lendRateAvg: Array,
  lendRateMax: Array,
  lendRateMax: Array,
})

const chartData = {
  labels: ['고정 금리', '변동 금리'],
  datasets: [
    {
      label: '전월 취급 평균 금리',
      data: props.lendRateAvg,
      backgroundColor: colors.grey.base,
      stack: 'Stack 0'
    },
    {
      label: '최저 대출 금리',
      data: props.lendRateMax,
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
      text: `<${props.title}> 상품의 대출 금리`
    },
  },
  responsive: true,
  scales: {
    x: {
      stacked: true,
      ticks: {
        maxRotation: 0,
        minRotation: 0,
        font: {
          size: 10
        }
      }
    },
  },
})
</script>


<style scoped>

</style>