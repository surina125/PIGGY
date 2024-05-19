<template>
  <div>
    <button @click="showPostCreate">글쓰기</button>
    <div v-if="isCreatingPost">
      <!-- create 창 닫으면 다시 글쓰기 버튼 활성화 -->
      <PostCreate @close="isCreatingPost = false"/>
    </div>
    <div v-if="!isCreatingPost">
      <div v-for="post in post_lists" :key="post.id">
        <p>{{ post.title }}</p>
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, defineAsyncComponent, onMounted } from 'vue';
import axios from 'axios';

// 동적으로 컴포넌트 불러옴
const PostCreate = defineAsyncComponent(() => import('@/components/Community/PostCreate.vue'));

const post_lists = ref([]);
const isCreatingPost = ref(false);


const postInfo = function() {
  axios.get('http://127.0.0.1:8000/community/')
  .then(response => {
    post_lists.value = response.data
  })
  .catch(error => {
    console.log(error)
  })
  
}


onMounted(postInfo);

function showPostCreate() {
  isCreatingPost.value = true;
}
</script>

<style scoped>
/* 스타일링 */
</style>