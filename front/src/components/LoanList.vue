<template>
  <div>
    <header class="d-flex justify-space-between">
      <h1><span class="color">주택담보대출</span> 검색하기</h1>
      <div class="w-50 d-flex align-center">
        <v-btn-toggle
          v-model="selectedTypeMrtg"
          variant="outlined"
          color="#1089FF"
          group
          class="mb-5 mx-5"
        >
          <v-btn value="아파트">
            아파트
          </v-btn>
          <v-btn value="아파트외">
            아파트 외
          </v-btn>
        </v-btn-toggle>

        <v-select
          variant="outlined"
          color="#1089FF"
          label="은행"
          :items="banks"
          v-model="selectedBank"
          @update:modelValue="clickBank"
        ></v-select>
      </div>
      
    </header>
    <v-divider class="my-3"></v-divider>

    <v-dialog v-model="dialog" width="800">
      <v-card v-if="selectedLoan" class="py-5 px-3">
        <v-card-title class="d-flex align-center justify-space-between">
          <h3>{{ selectedLoan['금융 상품명'] }}</h3>
          <div v-if="userStore.isLogin">
            <v-btn
              v-if="isContractLoan"
              color="red"
              variant="flat"
              @click.prevent="deleteLoanUser"
            >가입 취소하기</v-btn>
            <v-btn
              v-else
              color="#1089FF"
              variant="flat"
              @click.prevent="addLoanUser"
            >가입하기</v-btn>
          </div>
        </v-card-title>

        <v-card-text>
          <v-table>
            <tbody>
              <tr
                v-for="(value, key) in selectedLoan"
                :key="key"
              >
                <td width="28%" class="font-weight-bold">{{ key }}</td>
                <td v-if="key === '대출 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                <td v-else>{{ value }}</td>
              </tr>
            </tbody>
          </v-table>
          <v-divider class="my-3"></v-divider>

          <div class="mx-auto">
            <BarChartDetail
              :title="`${selectedLoanSimple.fin_prdt_nm} (아파트)`"
              :average-intr-rate="averageIntrRate"
              :intr-rate="intrRateF"
              :intr-rate2="intrRate2F"
            />
            <BarChartDetail
              :title="`${selectedLoanSimple.fin_prdt_nm} (아파트 외)`"
              :average-intr-rate="averageIntrRate"
              :intr-rate="intrRateS"
              :intr-rate2="intrRate2S"
            />
            <p class="text-caption">* 개월별 평균 예금 금리는 2023년 11월 기준입니다.</p>
            <p class="text-caption">* 차트에 없는 이자율은 상품에 존재하지 않는 옵션입니다.</p>
          </div>

        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="#1089FF" variant="text" @click="close">
            닫기
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-data-table-virtual
      v-if="loanLength !== 0"
      :headers="headers"
      fixed-header
      :items-length="loanLength"
      :items="loans"
      item-value="fin_prdt_cd"
      height="600"
      class="table elevation-6"
    >
      <template v-slot:item="{ item }">
        <tr @click="clickRow(item)">
          <td>{{ item['dcls_month'] }}</td>
          <td>{{ item['kor_co_nm'] }}</td>
          <td align="center">{{ item['fin_prdt_nm'] }}</td>
          <td align="center">{{ item['lend_rate_type_nm'] }}</td>
          <td align="center">{{ item['lend_rate_min'] }}</td>
          <td align="center">{{ item['lend_rate_max'] }}</td>
          <td align="center">{{ item['lend_rate_avg'] }}</td>
        </tr>
      </template>
    </v-data-table-virtual>
    
    <div v-else class="loading">
      <v-progress-circular
        color="#1089FF"
        indeterminate
        size="80"
        ></v-progress-circular>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/users'
import BarChartDetail from '@/components/BarChartDetail.vue'
import axios from 'axios'

const headers = [
  { title: '공시 제출일', align: 'start', sortable: false, width:'10%',key: 'dcls_month' },
  { title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
  { title: '상품명', align: 'center', sortable: false, width:'32%', key: 'fin_prdt_nm' },
  { title: '대출금리유형', align: 'center', sortable: false, width:'32%', key: 'lend_rate_type_nm' },
  { title: '최저 대출금리 (Click to sort)', align: 'end', width:'12%', key: 'lend_rate_min' },
  { title: '최고 대출금리 (Click to sort)', align: 'end', width:'12%', key: 'lend_rate_max' },
  { title: '전월 취급 평균금리 (Click to sort)', align: 'end',  width:'12%', key: 'lend_rate_avg' },
]

const results = ref()
const loans = ref([])
const loanLength = computed(() => {
  return loans.value.length
})
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedLoanSimple = ref()
const selectedLoan = ref()
const selectedLoanCode = computed(() => {
  return selectedLoanSimple.value?.['fin_prdt_cd']
})
const dialog = ref(false)

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRateF = ref([null, null, null, null])
const intrRate2F = ref([null, null, null, null])
const intrRateS = ref([null, null, null, null])
const intrRate2S = ref([null, null, null, null])

const selectedTypeMrtg = ref('아파트')

const isContractLoan = computed(() => {
  return userStore.userInfo?.contract_loan.some(e => e['fin_prdt_cd'] === selectedLoanCode.value)
})

const userStore = useUserStore()
const router = useRouter()

const makeItems = function (item) {
  const result = {
    'fin_prdt_cd': item['fin_prdt_cd'],
    'dcls_month': item['dcls_month'],
    'kor_co_nm': item['kor_co_nm'],
    'fin_prdt_nm': item['fin_prdt_nm'],
    'lend_rate_type_nm': null,
    'lend_rate_min': null,
    'lend_rate_max': null,
    'lend_rate_avg': null,
  }

  for (const option of item['loanoption_set']) {
    const mrtgTypeNm = option['mrtg_type_nm']
    if (mrtgTypeNm === selectedTypeMrtg.value) {
      result['lend_rate_type_nm'] = option['lend_rate_type_nm']
      result['lend_rate_min'] = option['lend_rate_min']
      result['lend_rate_max'] = option['lend_rate_max']
      result['lend_rate_avg'] = option['lend_rate_avg']
       
    }
  }

  return result
}

const getAllLoan = function () {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/fin_products/loan_list/`
  })
    .then((res) => {
      results.value = res.data
      console.log(results.value[0])
      for (const item of results.value){
        loans.value.push(makeItems(item))
        if (!banks.value.includes(item['kor_co_nm'])) {
          banks.value.push(item['kor_co_nm'])
        }
      }
      // console.log(loans.value)
      // console.log(banks.value)
    })
}

onMounted(() => {
  getAllLoan()
})

const clickBank = function () {
  if (selectedBank.value === '전체 보기') {
    getAllLoan()
  } else {
    axios({
      method: 'get',
      url: `${userStore.API_URL}/financial/get_bank_loan/${selectedBank.value}/`
    })
      .then((res) => {
        loans.value = []
        const results = res.data
        for (const item of results){
          loans.value.push(makeItems(item))
        }
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

watch(selectedTypeMrtg, () => {
  loans.value = []
  selectedBank.value = '전체 보기'
  for (const item of results.value){
    loans.value.push(makeItems(item))
    if (!banks.value.includes(item['kor_co_nm'])) {
      banks.value.push(item['kor_co_nm'])
    }
  }
})

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  // router.push({ name: 'loanDetail', params: { loanCode: data['loan_code']}})
  selectedLoanSimple.value = data
  intrRateF.value = []
  intrRate2F.value = []
  intrRateS.value = []
  intrRate2S.value = []
  getLoan()
  dialog.value = true
}

const getLoan = function () {
  const fin_prdt_cd = selectedLoanSimple.value['fin_prdt_cd']
  axios({
    method: 'get',
    url: `${userStore.API_URL}/financial/loan_list/${selectedLoanCode.value}/`
  })
    .then((res) => {
      const data = res.data
      selectedLoan.value = {
        '가입자 수 (MYFI 기준)': data.contract_user.length,
        '공시 제출월': data['dcls_month'],
        '금융 회사명': data['kor_co_nm'],
        '금융 상품명': data['fin_prdt_nm'],
        // '가입 방법': data['join_way'],
        '중도 상환 수수료': data['erly_rpay_fee'],
        '연체 이자율': data['dly_rate'],
        '만기 후 이자율': data['mtrt_int'],
        // '만기 후 이자율': data['mtrt_int'],
        // '우대 조건': data['spcl_cnd'],
        // '가입 대상': data['join_member'],
        // '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
        '대출 한도': data['loan_lmt'],
        // '기타 유의사항': data['etc_note']
      }

      const optionList = res.data.loanoption_set

      for (const option of optionList) {
        if (option.mrtg_type_nm === '아파트') {
          if (option.save_trm === "6") {
            intrRateF.value[0] = option.intr_rate
            intrRate2F.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRateF.value[1] = option.intr_rate
            intrRate2F.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRateF.value[2] = option.intr_rate
            intrRate2F.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRateF.value[3] = option.intr_rate
            intrRate2F.value[3] = option.intr_rate2
          }
        } else {
          if (option.save_trm === "6") {
            intrRateS.value[0] = option.intr_rate
            intrRate2S.value[0] = option.intr_rate2
          } else if (option.save_trm === "12") {
            intrRateS.value[1] = option.intr_rate
            intrRate2S.value[1] = option.intr_rate2
          } else if (option.save_trm === "24") {
            intrRateS.value[2] = option.intr_rate
            intrRate2S.value[2] = option.intr_rate2
          } else if (option.save_trm === "36") {
            intrRateS.value[3] = option.intr_rate
            intrRate2S.value[3] = option.intr_rate2
          }
        }
      }

    })
    .catch((err) => {
      console.log(err)
    })
}

const addLoanUser = function () {
  axios({
    method: 'post',
    url: `${userStore.API_URL}/fin_products/loan_list/${selectedLoanCode.value}/contract/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      userStore.getUserInfo(userStore.userInfo.username)
      const answer = window.confirm('저장이 완료되었습니다.\n가입 상품 관리 페이지로 가시겠습니까?')
      if (answer) {
        router.push({ name: 'productManage', params: { username: userStore.userInfo.username }})
      }
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteLoanUser = function () {
  axios({
    method: 'delete',
    url: `${userStore.API_URL}/fin_products/loan_list/${selectedLoanCode.value}/contract/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then((res) => {
      userStore.getUserInfo(userStore.userInfo.username)
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style scoped>
.loading { 
  display: flex;
  height: 80vh;
  align-items: center;
  justify-content: center;
}

tbody > tr {
  transition: 200ms;
  cursor: pointer;
}

tbody > tr:hover {
  background-color: rgb(247, 250, 253);
  color: #1089FF;
}

.table {
  border-radius: 10px;
}
</style>