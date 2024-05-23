<template>
  <div class="container mt-5">
    <!-- Carousel -->
    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div 
          v-for="(prd, index) in recommendStore.reco1D" 
          :key="index" 
          :class="['carousel-item', { active: index === 0 }]">
          <div class="card mx-auto" style="width: 18rem;">
            <div class="card-header bg-primary text-white">
              <h5 class="card-title">{{ prd.fin_prdt_nm }}</h5>
              <h6 class="card-subtitle mb-2">{{ prd.kor_co_nm }}</h6>
            </div>
            <div class="card-body">
              <p class="card-text">
                <strong>공시제출일: </strong>{{ prd.dcls_month }}<br>
                <strong>가입방법: </strong>{{ prd.join_way }}<br>
                <strong>가입대상: </strong>{{ prd.join_member }}<br>
                <strong>최고 한도: </strong>{{ prd.max_limit }}<br>
                <strong>만기 후 이자율: </strong>{{ prd.mtrt_int }}<br>
                <strong>우대조건: </strong>{{ prd.spcl_cnd }}<br>
                <strong>기타 유의사항: </strong>{{ prd.etc_note }}
              </p>
              <div class="chart-container">
                <Bar class="chart" :data="getChartData(prd)" :options="options" />
              </div>
            </div>
            <div class="card-footer bg-light text-muted">
              <p class="mb-1"><strong>6개월 금리: </strong>{{ getInterestRate(prd, '6') }}%</p>
              <p class="mb-1"><strong>12개월 금리: </strong>{{ getInterestRate(prd, '12') }}%</p>
              <p class="mb-1"><strong>24개월 금리: </strong>{{ getInterestRate(prd, '24') }}%</p>
              <p class="mb-1"><strong>36개월 금리: </strong>{{ getInterestRate(prd, '36') }}%</p>
            </div>
          </div>
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRecommendStore } from '@/stores/recommend.js'
import { ref } from 'vue'
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

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const recommendStore = useRecommendStore()

// 기간별로 저축금리 가져오기
const getInterestRate = (prd, term) => {
  if (!prd || !prd.depositoption_set) return '-';

  const option = prd.depositoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
}

// 기간별로 최고 우대금리 가져오기
const getInterestRate2 = (prd, term) => {
  if (!prd || !prd.depositoption_set) return '-';

  const option = prd.depositoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate2 : '-';
}

// 차트 데이터 생성
const getChartData = (prd) => {
  return {
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
          parseFloat(getInterestRate(prd, '6')) || 0,
          parseFloat(getInterestRate(prd, '12')) || 0,
          parseFloat(getInterestRate(prd, '24')) || 0,
          parseFloat(getInterestRate(prd, '36')) || 0
        ]
      },
      {
        label: '최고 우대 금리',
        backgroundColor: '#aad1e6',
        data: [
          parseFloat(getInterestRate2(prd, '6')) || 0,
          parseFloat(getInterestRate2(prd, '12')) || 0,
          parseFloat(getInterestRate2(prd, '24')) || 0,
          parseFloat(getInterestRate2(prd, '36')) || 0
        ]
      },
    ]
  }
}

// 차트 옵션 설정
const options = {
  responsive: true,
  maintainAspectRatio: false, // 세로 길이를 고정
  aspectRatio: 2, // 세로길이 2로 설정함, 가로는 부모에 따라 조정됨
}
</script>

<style scoped>
.card {
  margin: 10px auto;
  max-width: 350px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #007bff;
  color: white;
  padding: 15px;
  border-bottom: none;
}

.card-body {
  padding: 15px;
}

.card-footer {
  background-color: #f8f9fa;
  padding: 10px;
  border-top: none;
}

.chart-container {
  position: relative;
  height: 200px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
