<template>
  <div class="chart-page">
    <Bar :data="data" :options="options" style="width: 50px; height: 50px;" />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import { useDepositStore } from '@/stores/deposit'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default defineComponent({
  name: 'DepositChart',
  components: {
    Bar
  },

  setup() {

    // 특정 저축 기간에 대한 저축 금리 찾는 함수
    const getInterestRate = (deposit, term) => {
      if (deposit) {
        const option = deposit.depositoption_set.find(option => option.save_trm === term)
        return option ? option.intr_rate : 0
      }
      return 0
    }
    // 특정 저축 기간에 대한 최고우대 금리 찾는 함수
    const getInterestRate2 = (deposit, term) => {
      if (deposit) {
        const option = deposit.depositoption_set.find(option => option.save_trm === term)
        return option ? option.intr_rate2 : 0
      }
      return 0
    }

    const store = useDepositStore()


    const data = {
      labels: [
        '6개월',
        '12개월',
        '24개월',
        '36개월',
      ],
      datasets: [
        {
          label: '저축 금리',
          backgroundColor: '#f87979',
          data: [
            getInterestRate(store.deposit, '6'), 
            getInterestRate(store.deposit, '12'), 
            getInterestRate(store.deposit, '24'), 
            getInterestRate(store.deposit, '36')
          ]
        },
        {
          label: '최고 우대 금리',
          backgroundColor: '#f87979',
          data: [
            getInterestRate2(store.deposit, '6'), 
            getInterestRate2(store.deposit, '12'), 
            getInterestRate2(store.deposit, '24'), 
            getInterestRate2(store.deposit, '36')
          ]
        },
      ]
    };

    const options = {
      responsive: true,
      maintainAspectRatio: false
    };

    return {
      data, options
    };
  }
});
</script>

<style scoped>
.chart-page {
  width: 80vh;
  height: 30vw;
}
</style>
