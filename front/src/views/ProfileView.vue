<template>
  <div class="profile-container bg-light text-dark rounded mt-5 p-4 shadow">
    <div class="profile-pic-container mb-4 text-center">
      <img :src="userProfilePic" alt="프로필 이미지" class="profile-pic rounded-circle shadow" />
    </div>
    <div class="text-center mb-4">
      <h1>{{ authStore.userData.nickname }}님의 프로필</h1>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <div class="form-group">
          <label for="age"><strong>나이</strong></label>
          <p>{{ authStore.userData.age }}</p>
        </div>
        <div class="form-group">
          <label for="annual_income"><strong>연간 소득</strong></label>
          <p>{{ authStore.userData.annual_income }}</p>
        </div>
        <div class="form-group">
          <label for="property"><strong>자산</strong></label>
          <p>{{ authStore.userData.property }}</p>
        </div>
        <div class="form-group">
          <label for="main_bank"><strong>주 은행</strong></label>
          <p>{{ authStore.userData.main_bank }}</p>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">예금 가입 상품</h5>
        <hr>
        <div v-for="product in contractDepositProduct" :key="product.id" class="product-item">
          <p>{{ product.fin_prdt_nm }}({{ product.kor_co_nm }})
            <button type="button" class="btn btn-danger btn-sm" v-if="isDespositContracted(product.fin_prdt_cd)" @click="delDepositContract(product.fin_prdt_cd)">X</button>
          </p>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">적금 가입 상품</h5>
        <hr>
        <div v-for="product in contractSavingProduct" :key="product.id" class="product-item">
          <p>{{ product.fin_prdt_nm }}({{ product.kor_co_nm }})
            <button type="button" class="btn btn-danger btn-sm" v-if="isSavingContracted(product.fin_prdt_cd)" @click="delSavingContract(product.fin_prdt_cd)">X</button>
          </p>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">대출 가입 상품</h5>
        <hr>
        <div v-for="product in contractLoanProduct" :key="product.id" class="product-item">
          <p>{{ product.fin_prdt_nm }}({{ product.kor_co_nm }})
            <button type="button" class="btn btn-danger btn-sm" v-if="isLoanContracted(product.fin_prdt_cd)" @click="delLoanContract(product.fin_prdt_cd)">X</button>
          </p>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">예금 관심 상품</h5>
        <hr>
        <div v-for="product in likeDepositProduct" :key="product.id" class="product-item">
          <p>{{ product.fin_prdt_nm }}({{ product.kor_co_nm }})
            <button type="button" class="btn btn-danger btn-sm" v-if="isDespositLiked(product.fin_prdt_cd)" @click="delDepositLiked(product.fin_prdt_cd)">X</button>
          </p>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">적금 관심 상품</h5>
        <hr>
        <div v-for="product in likeSavingProduct" :key="product.id" class="product-item">
          <p>{{ product.fin_prdt_nm }}({{ product.kor_co_nm }})
            <button type="button" class="btn btn-danger btn-sm" v-if="isSavingLiked(product.fin_prdt_cd)" @click="delSavingLiked(product.fin_prdt_cd)">X</button>
          </p>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">대출 관심 상품</h5>
        <hr>
        <div v-for="product in likeLoanProduct" :key="product.id" class="product-item">
          <p>{{ product.fin_prdt_nm }}({{ product.kor_co_nm }})
            <button type="button" class="btn btn-danger btn-sm" v-if="isLoanLiked(product.fin_prdt_cd)" @click="delLoanLiked(product.fin_prdt_cd)">X</button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { useDepositStore } from '@/stores/deposit'
import { useSavingStore } from '@/stores/saving'
import { useLoanStore } from '@/stores/loan'

const contractDepositProduct = ref([])
const contractSavingProduct = ref([])
const contractLoanProduct = ref([])
const likeDepositProduct = ref([])
const likeSavingProduct = ref([])
const likeLoanProduct = ref([])

const authStore = useAuthStore()
const depositStore = useDepositStore()
const savingStore = useSavingStore()
const loanStore = useLoanStore()

const isDespositContracted = (fin_prdt_cd) => {
  return contractDepositProduct.value.some(product => product.fin_prdt_cd === fin_prdt_cd);
}

const isSavingContracted = (fin_prdt_cd) => {
  return contractSavingProduct.value.some(product => product.fin_prdt_cd === fin_prdt_cd);
}

const isLoanContracted = (fin_prdt_cd) => {
  return contractLoanProduct.value.some(product => product.fin_prdt_cd === fin_prdt_cd);
}

const isDespositLiked = (fin_prdt_cd) => {
  return likeDepositProduct.value.some(product => product.fin_prdt_cd === fin_prdt_cd);
}

const isSavingLiked = (fin_prdt_cd) => {
  return likeSavingProduct.value.some(product => product.fin_prdt_cd === fin_prdt_cd);
}

const isLoanLiked = (fin_prdt_cd) => {
  return likeLoanProduct.value.some(product => product.fin_prdt_cd === fin_prdt_cd);
}

const userProfilePic = authStore.userData.profile_img ? `${authStore.userData.profile_img}` : '/media/image/user.png';

const contractDepositList = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/fin_products/dep/contract/search/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
    .then((response) => {
      contractDepositProduct.value = response.data
      console.log(contractDepositProduct.value)
    })
    .catch((error) => {
      console.log(error)
    })
}
const contractSavingList = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/fin_products/sav/contract/search/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
    .then((response) => {
      contractSavingProduct.value = response.data
      console.log(contractSavingProduct.value)
    })
    .catch((error) => {
      console.log(error)
    })
}

const contractLoanList = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/fin_products/loa/contract/search/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
    .then((response) => {
      contractLoanProduct.value = response.data
      console.log(contractLoanProduct.value)
    })
    .catch((error) => {
      console.log(error)
    })
}

const delDepositContract = (fin_prdt_cd) => {
  const idx = contractDepositProduct.value.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {
    axios({
      method: 'post',
      url: `${depositStore.API_URL}/fin_products/deposit/contract/${fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        console.log(response.data)
        contractDepositProduct.value.splice(idx, 1)
        contractDepositList()

        depositStore.contractedDeposit = depositStore.contractedDeposit.filter(obj => obj.fin_prdt_cd !== fin_prdt_cd)
      })
      .catch(error => {
        console.log(error)
      })
  }
}

const delSavingContract = (fin_prdt_cd) => {
  const idx = contractSavingProduct.value.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {
    axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving/contract/${fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        contractSavingProduct.value.splice(idx, 1)
        contractSavingList()

        savingStore.contractedSaving = savingStore.SavingDeposit.filter(obj => obj.fin_prdt_cd !== fin_prdt_cd)
      })
      .catch(error => {
        console.log(error)
      })
  }
}

const delLoanContract = (fin_prdt_cd) => {
  const idx = contractLoanProduct.value.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {
    axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan/contract/${fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        contractLoanProduct.value.splice(idx, 1)
        contractLoanList()

        loanStore.contractedLoan = loanStore.contractedLoan.filter(obj => obj.fin_prdt_cd !== fin_prdt_cd)
      })
      .catch(error => {
        console.log(error)
      })
  }
}

const likeDepositList = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/fin_products/dep/like/search/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
    .then((response) => {
      likeDepositProduct.value = response.data
      console.log(likeDepositProduct.value)
    })
    .catch((error) => {
      console.log(error)
    })
}

const likeSavingList = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/fin_products/sav/like/search/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
    .then((response) => {
      likeSavingProduct.value = response.data
      console.log(likeSavingProduct.value)
    })
    .catch((error) => {
      console.log(error)
    })
}

const likeLoanList = () => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/fin_products/loa/like/search/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
    .then((response) => {
      likeLoanProduct.value = response.data
      console.log(likeLoanProduct.value)
    })
    .catch((error) => {
      console.log(error)
    })
}

const delDepositLiked = (fin_prdt_cd) => {
  const idx = likeDepositProduct.value.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {
    axios({
      method: 'post',
      url: `${depositStore.API_URL}/fin_products/deposit/like/${fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        likeDepositProduct.value.splice(idx, 1)
        likeDepositList()

        depositStore.savedDeposit = depositStore.savedDeposit.filter(obj => obj.fin_prdt_cd !== fin_prdt_cd)

      })
      .catch(error => {
        console.log(error)
      })
  }
}
const delSavingLiked = (fin_prdt_cd) => {
  const idx = likeSavingProduct.value.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {
    axios({
      method: 'post',
      url: `${savingStore.API_URL}/fin_products/saving/like/${fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        likeSavingProduct.value.splice(idx, 1)
        likeSavingList()

        savingStore.savedSaving = savingStore.savedSaving.filter(obj => obj.fin_prdt_cd !== fin_prdt_cd)

      })
      .catch(error => {
        console.log(error)
      })
  }
}

const delLoanLiked = (fin_prdt_cd) => {
  const idx = likeLoanProduct.value.findIndex((prd) => prd.fin_prdt_cd === fin_prdt_cd)
  if (idx !== -1) {
    axios({
      method: 'post',
      url: `${loanStore.API_URL}/fin_products/loan/like/${fin_prdt_cd}/`,
      data: {
        fin_prdt_cd: fin_prdt_cd
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(response => {
        likeLoanProduct.value.splice(idx, 1)
        likeLoanList()

        loanStore.savedLoan = loanStore.savedLoan.filter(obj => obj.fin_prdt_cd !== fin_prdt_cd)

      })
      .catch(error => {
        console.log(error)
      })
  }
}

onMounted(() => {
  contractDepositList();
  contractSavingList();
  contractLoanList();
  likeDepositList();
  likeSavingList();
  likeLoanList();
});
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  min-width: 300px;
  margin: 0 auto;
}

.profile-pic-container {
  position: relative;
}

.profile-pic {
  width: 150px;
  height: 150px;
  object-fit: cover;
}

.form-group {
  margin-bottom: 1rem;
}

.card {
  border: none;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.product-item p {
  margin: 0;
}

.btn-danger {
  font-size: 0.8rem;
}
</style>
