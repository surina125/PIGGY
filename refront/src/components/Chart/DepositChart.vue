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

// Chart.js 모듈을 등록합니다.
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default defineComponent({
  name: 'DepositChart',
  components: {
    Bar
  },
  // 부모 컴포넌트로부터 받은 deposit prop을 정의합니다.
  props: {
    deposit: Object
  },
  // setup 함수를 사용하여 컴포넌트의 데이터와 옵션을 설정합니다.
  setup(props) {
    // setup 함수 내에서 console.log()를 사용하여 deposit을 확인합니다.
    console.log('Received deposit in DepositChart:', props.deposit.value);

    // 특정 기간에 대한 저축 금리를 가져오는 함수
    const getInterestRate = (term) => {
      const option = props.deposit.value.depositoption_set.find(option => option.save_trm === term)
      return option ? option.intr_rate : 0
    }

    // 특정 기간에 대한 최고 우대 금리를 가져오는 함수
    const getInterestRate2 = (term) => {
      const option = props.deposit.value.depositoption_set.find(option => option.save_trm === term)
      return option ? option.intr_rate2 : 0
    }

    // 차트에 표시할 데이터
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
            getInterestRate('6'), 
            getInterestRate('12'), 
            getInterestRate('24'), 
            getInterestRate('36')
          ]
        },
        {
          label: '최고 우대 금리',
          backgroundColor: '#aad1e6',
          data: [
            getInterestRate2('6'), 
            getInterestRate2('12'), 
            getInterestRate2('24'), 
            getInterestRate2('36')
          ]
        },
      ]
    };

    // 차트 옵션 설정
    const options = {
      responsive: true,
      maintainAspectRatio: false
    };

    // setup 함수에서 반환하는 객체에 데이터와 옵션을 포함하여 반환합니다.
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
