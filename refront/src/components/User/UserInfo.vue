<template>
  <div class="profile-container bg-light text-dark rounded mt-5 p-4 shadow">
    <div class="profile-pic-container mb-4 text-center" v-if="userProfilePic">
      <img :src="userProfilePic" alt="No Image" class="profile-pic rounded-circle shadow" />
    </div>
    <div class="text-center mb-2">
      <button @click="changeProfilePic" class="btn btn-light change-profile-pic-btn">프로필 사진 변경</button>
    </div>
    <form @submit.prevent="updateProfile">
      <div class="form-group">
        <label for="age"><strong>나이</strong></label>
        <input type="number" v-model="user.age" class="form-control" id="age" />
      </div>
      <div class="form-group">
        <label for="annual_income"><strong>연간 소득</strong></label>
        <input type="number" v-model="user.annual_income" class="form-control" id="annual_income" />
      </div>
      <div class="form-group">
        <label for="property"><strong>자산</strong></label>
        <input type="number" v-model="user.property" class="form-control" id="property" />
      </div>
      <div class="form-group">
        <label for="main_bank"><strong>주 은행</strong></label>
        <input type="text" v-model="user.main_bank" class="form-control" id="main_bank" />
      </div>
      <div class="text-center mb-4">
        <button type="submit" class="btn btn-primary">프로필 수정</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

const authStore = useAuthStore()
const user = ref({ ...authStore.userData })
const router = useRouter()

const selectedFile = ref(null)
const selectedFileUrl = ref(null)

const userProfilePic = computed(() => {
  return selectedFileUrl.value || user.value.profile_img
})

const changeProfilePic = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => {
    selectedFile.value = e.target.files[0]
    if (selectedFile.value) {
      selectedFileUrl.value = URL.createObjectURL(selectedFile.value)
    }
  }
  input.click()
}

const updateProfile = () => {
  const formData = new FormData()
  if (selectedFile.value) {
    formData.append('profile_img', selectedFile.value)
  }
  formData.append('age', user.value.age)
  formData.append('annual_income', user.value.annual_income)
  formData.append('property', user.value.property)
  formData.append('main_bank', user.value.main_bank)

  axios.patch(`http://localhost:8000/users/user/${user.value.username}/`, formData, {
    headers: {
      Authorization: `Token ${authStore.token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
    .then((response) => {
      if (response && response.data) {
        user.value = { ...response.data } // 상태 동기화
        authStore.userData = response.data // 상태 동기화
        selectedFileUrl.value = null // 선택한 파일 URL을 초기화합니다.
        alert('프로필이 성공적으로 수정되었습니다.')

        router.push({ name: 'profile', params: { userId: authStore.userData.pk } })
      }
    })
    .catch((error) => {
      console.error('Error updating profile:', error)
      alert('프로필 수정 중 오류가 발생했습니다.')
    })
}
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

.change-profile-pic-btn {
  border: 2px solid #ccc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
