<template>
  <div class="recoResult-page pt-3 pb-5">
    <!-- 예금 상품 카드 -->
    <div class="container mt-5" style="background-color: white; width: 100%;">
      <h3 class="section-title">추천하는 예금 상품</h3>
      <div class="position-relative">
        <div class="arrow arrow-left" @click="scrollLeft('deposit')">‹</div>
        <div class="card-container card-container-deposit">
          <div 
            v-for="(prd, index) in recommendStore.reco1D" 
            :key="index" 
            class="card card-deposit mx-2" style="width: 18rem;">
            <div class="card-header card-header-deposit bg-primary text-white d-flex flex-column justify-content-center">
              <h5 class="card-title text-center">{{ prd.fin_prdt_nm }}</h5>
              <h6 class="card-subtitle mb-2 text-center">{{ prd.kor_co_nm }}</h6>
            </div>
            <div class="card-body card-body-deposit">
              <div class="chart-container chart-container-deposit">
                <Bar class="chart" :data="getDepositChartData(prd)" :options="options" />
              </div>
            </div>
          </div>
        </div>
        <div class="arrow arrow-right" @click="scrollRight('deposit')">›</div>
      </div>
    </div>

    <!-- 적금 상품 카드 -->
    <div class="container mt-5" style="background-color: white; width: 100%;">
      <h3 class="section-title">추천하는 적금 상품</h3>
      <div class="position-relative">
        <div class="arrow arrow-left" @click="scrollLeft('saving')">‹</div>
        <div class="card-container card-container-saving">
          <div 
            v-for="(prd, index) in recommendStore.reco1S" 
            :key="index" 
            class="card card-saving mx-2" style="width: 18rem;">
            <div class="card-header card-header-saving bg-success text-white d-flex flex-column justify-content-center">
              <h5 class="card-title text-center">{{ prd.fin_prdt_nm }}</h5>
              <h6 class="card-subtitle mb-2 text-center">{{ prd.kor_co_nm }}</h6>
            </div>
            <div class="card-body card-body-saving">
              <div class="chart-container chart-container-saving">
                <Bar class="chart" :data="getSavingChartData(prd)" :options="options" />
              </div>
            </div>
          </div>
        </div>
        <div class="arrow arrow-right" @click="scrollRight('saving')">›</div>
      </div>
    </div>

    <!-- 주택담보대출 상품 카드 -->
    <div class="container mt-5" style="background-color: white; width: 100%;">
      <h3 class="section-title">추천하는 주택담보대출 상품</h3>
      <div class="position-relative">
        <div class="arrow arrow-left" @click="scrollLeft('mortgage')">‹</div>
        <div class="card-container card-container-mortgage">
          <div 
            v-for="(prd, index) in recommendStore.reco1L" 
            :key="index" 
            class="card card-mortgage mx-2" style="width: 18rem;">
            <div class="card-header card-header-mortgage bg-danger text-white d-flex flex-column justify-content-center">
              <h5 class="card-title text-center">{{ prd.fin_prdt_nm }}</h5>
              <h6 class="card-subtitle mb-2 text-center">{{ prd.kor_co_nm }}</h6>
            </div>
            <div class="card-body card-body-mortgage">
              <div class="chart-container chart-container-mortgage">
                <Bar v-if="prd.loas_type === '아파트'" class="chart" :data="getApartmentChartData(prd)" :options="options"/>
                <Bar v-else class="chart" :data="getNonApartmentChartData(prd)" :options="options"/>
              </div>
            </div>
          </div>
        </div>
        <div class="arrow arrow-right" @click="scrollRight('mortgage')">›</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useLoanStore } from '@/stores/loan.js'
import { useAuthStore } from '@/stores/auth.js'
import { useRecommendStore } from '@/stores/recommend'
import { ref, computed } from 'vue'
import axios from 'axios'
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

const recommendStore = useRecommendStore()
const loanStore = useLoanStore()
const authStore = useAuthStore()

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const scrollLeft = (type) => {
  const container = document.querySelector(`.card-container-${type}`);
  container.scrollBy({ left: -container.clientWidth / 4, behavior: 'smooth' });
}

const scrollRight = (type) => {
  const container = document.querySelector(`.card-container-${type}`);
  container.scrollBy({ left: container.clientWidth / 4, behavior: 'smooth' });
}

// 기간별로 저축금리 가져오기
const getDepositInterestRate = (prd, term) => {
  if (!prd || !prd.depositoption_set) return '-';

  const option = prd.depositoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
}

// 기간별로 최고 우대금리 가져오기
const getDepositInterestRate2 = (prd, term) => {
  if (!prd || !prd.depositoption_set) return '-';

  const option = prd.depositoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate2 : '-';
}

// 기간별로 적금 금리 가져오기
const getSavingInterestRate = (prd, term) => {
  if (!prd || !prd.savingoption_set) return '-';

  const option = prd.savingoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate : '-';
}

// 기간별로 최고 우대금리 가져오기
const getSavingInterestRate2 = (prd, term) => {
  if (!prd || !prd.savingoption_set) return '-';

  const option = prd.savingoption_set.find(option => option.save_trm === term);
  return option ? option.intr_rate2 : '-';
}

// 예금 차트 데이터 생성
const getDepositChartData = (prd) => {
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
          parseFloat(getDepositInterestRate(prd, '6')) || 0,
          parseFloat(getDepositInterestRate(prd, '12')) || 0,
          parseFloat(getDepositInterestRate(prd, '24')) || 0,
          parseFloat(getDepositInterestRate(prd, '36')) || 0
        ]
      },
      {
        label: '최고 우대 금리',
        backgroundColor: '#aad1e6',
        data: [
          parseFloat(getDepositInterestRate2(prd, '6')) || 0,
          parseFloat(getDepositInterestRate2(prd, '12')) || 0,
          parseFloat(getDepositInterestRate2(prd, '24')) || 0,
          parseFloat(getDepositInterestRate2(prd, '36')) || 0
        ]
      },
    ]
  }
}

// 적금 차트 데이터 생성
const getSavingChartData = (prd) => {
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
          parseFloat(getSavingInterestRate(prd, '6')) || 0,
          parseFloat(getSavingInterestRate(prd, '12')) || 0,
          parseFloat(getSavingInterestRate(prd, '24')) || 0,
          parseFloat(getSavingInterestRate(prd, '36')) || 0
        ]
      },
      {
        label: '최고 우대 금리',
        backgroundColor: '#aad1e6',
        data: [
          parseFloat(getSavingInterestRate2(prd, '6')) || 0,
          parseFloat(getSavingInterestRate2(prd, '12')) || 0,
          parseFloat(getSavingInterestRate2(prd, '24')) || 0,
          parseFloat(getSavingInterestRate2(prd, '36')) || 0
        ]
      },
    ]
  }
}

// 대출 차트 데이터 생성
const getApartmentChartData = (prd) => {
  const apartmentData = prd.loanoption_set.filter(option => option.mrtg_type_nm === '아파트')
  const apartmentFixedRate = apartmentData.find(option => option.lend_rate_type_nm === '고정금리')
  const apartmentVariableRate = apartmentData.find(option => option.lend_rate_type_nm === '변동금리')

  return {
    labels: ['고정금리', '변동금리'],
    datasets: [
      {
        label: '최저 금리',
        backgroundColor: '#f87979',
        data: [
          apartmentFixedRate ? apartmentFixedRate.lend_rate_min : 0,
          apartmentVariableRate ? apartmentVariableRate.lend_rate_min : 0
        ]
      },
      {
        label: '최고 금리',
        backgroundColor: '#aad1e6',
        data: [
          apartmentFixedRate ? apartmentFixedRate.lend_rate_max : 0,
          apartmentVariableRate ? apartmentVariableRate.lend_rate_max : 0
        ]
      },
      {
        label: '전월 취급 평균금리',
        backgroundColor: '#82ca9d',
        data: [
          apartmentFixedRate ? apartmentFixedRate.lend_rate_avg : 0,
          apartmentVariableRate ? apartmentVariableRate.lend_rate_avg : 0
        ]
      }
    ]
  }
}

const getNonApartmentChartData = (prd) => {
  const nonApartmentData = prd.loanoption_set.filter(option => option.mrtg_type_nm !== '아파트')
  const nonApartmentFixedRate = nonApartmentData.find(option => option.lend_rate_type_nm === '고정금리')
  const nonApartmentVariableRate = nonApartmentData.find(option => option.lend_rate_type_nm === '변동금리')

  return {
    labels: ['고정금리', '변동금리'],
    datasets: [
      {
        label: '최저 금리',
        backgroundColor: '#f87979',
        data: [
          nonApartmentFixedRate ? nonApartmentFixedRate.lend_rate_min : 0,
          nonApartmentVariableRate ? nonApartmentVariableRate.lend_rate_min : 0
        ]
      },
      {
        label: '최고 금리',
        backgroundColor: '#aad1e6',
        data: [
          nonApartmentFixedRate ? nonApartmentFixedRate.lend_rate_max : 0,
          nonApartmentVariableRate ? nonApartmentVariableRate.lend_rate_max : 0
        ]
      },
      {
        label: '전월 취급 평균금리',
        backgroundColor: '#82ca9d',
        data: [
          nonApartmentFixedRate ? nonApartmentFixedRate.lend_rate_avg : 0,
          nonApartmentVariableRate ? nonApartmentVariableRate.lend_rate_avg : 0
        ]
      }
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
.recoResult-page {
  width: 100%;
  background-color: white;
}

.card {
  margin: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  color: white;
  padding: 15px;
  border-bottom: none;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100px; /* 제목 부분의 높이를 고정 */
}

.card-title, .card-subtitle {
  margin: 0;
}

.card-body {
  padding: 15px;
}

.chart-container {
  position: relative;
  height: 200px;
}

.chart {
  width: 100%;
  height: 100%;
}

.card-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  padding: 10px;
  scrollbar-width: none; /* Firefox */
}

.card-container::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.card-container-deposit, .card-container-saving, .card-container-mortgage {
  gap: 10px;
  justify-content: flex-start;
}

.card-container-deposit > .card, .card-container-saving > .card, .card-container-mortgage > .card {
  flex: 0 0 calc(25% - 10px);
}

.position-relative {
  position: relative;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2rem;
  color: rgba(0, 0, 0, 0.5);
  cursor: pointer;
  z-index: 1;
  user-select: none;
}

.arrow-left {
  left: 0;
}

.arrow-right {
  right: 0;
}

.arrow:hover {
  color: rgba(0, 0, 0, 0.8);
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}
</style>
