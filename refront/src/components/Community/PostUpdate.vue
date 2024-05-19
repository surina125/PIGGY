<template>
  <div>
    <h1>수정하기</h1>
    <form @submit.prevent="handleSubmit">
      <label for="title">제목:</label>
      <input type="text" id="title" v-model="title"/>
      <label for="content">내용:</label>
      <input type="text" id="content" v-model="content"/>

      <button type="submit" >게시글 수정</button>

    </form>
  </div>
</template>

<script setup>

import {ref} from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth.js'

const postStore = usePostStore()
const authStore = useAuthStore()
const title = ref('')
const content = ref('')
const router = useRouter()


function handleSubmit() {
  postStore.postUpdate({
    title: title.value,
    content: content.value
  })
  .then(() => {
    // 수정이 완료되면 상세 페이지로 이동
    router.push({
      name: 'postdetail',
      params: { postId: postStore.updatePostId }
    });
  })
  .catch((error) => {
    console.error(error);
  });
}

</script>

<style scoped>

</style>