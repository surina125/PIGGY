
<template>
  <div>
    <h1>글쓰기</h1>
    <form @submit.prevent="postCreate">
      <label for="title">제목:</label>
      <input type="text" id="title" v-model="title"/>
      <label for="content">내용:</label>
      <input type="text" id="content" v-model="content"/>

      <button type="submit">게시글 생성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth.js';
import { useRouter } from 'vue-router'

const authStore = useAuthStore();
const title = ref('');
const content = ref('');
const router = useRouter()


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
    console.log('Post created:', response.data)
    router.push({name:'postdetail', params:{postId:response.data.id}})
    
  })
  .catch(error => {
    console.error('Error creating post:', error);
  });
};
</script>

<style scoped>
/* Your SCSS styles here */
</style>
