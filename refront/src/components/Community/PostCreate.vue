<template>
  <div class="form-container mt-4 mb-3 community-page">
    <h2>게시글 작성</h2>
    <form @submit.prevent="postCreate">
      <div class="mb-3">
        <label for="title">제목</label>
        <input type="text" class="form-control" id="title" v-model="title" placeholder="제목을 입력해 주세요">
      </div>
      <div class="mb-3">
        <label for="content">내용</label>
        <textarea class="form-control" id="content" v-model="content" rows="5" placeholder="내용을 입력해 주세요"></textarea>
      </div>
      <div class="button-group">
        <button type="submit" class="btn btn-outline-secondary">저장</button>
        <button type="button" class="btn btn-outline-secondary" @click="goPostList">목록</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth.js';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const title = ref('');
const content = ref('');
const router = useRouter();

const postCreate = () => {
  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/community/post/create/',
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
    data: {
      title: title.value,
      content: content.value
    }
  })
  .then(response => {
    console.log('Post created:', response.data);
    router.push({ name: 'postdetail', params: { postId: response.data.id } });
  })
  .catch(error => {
    console.error('Error creating post:', error);
  });
};

const goPostList = function() {
  router.push({ name: 'community'})
}
</script>

<style scoped>
.form-container {
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 70%;
  margin: 0 auto;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
}

.form-control:focus {
  border-color: #333;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.button-group {
  text-align: right;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s, color 0.3s;
  margin-right: 10px;
}

.btn-outline-secondary {
  color: #333;
  border-color: #333;
}

.btn-outline-secondary:hover {
  color: #fff;
  background-color: #333;
}
</style>
