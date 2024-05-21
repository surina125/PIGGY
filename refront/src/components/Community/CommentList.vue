<template>
  <div>
    <h2>댓글 목록</h2>
    <div v-for="comment in postStore.commentInfos" :key="comment.id">
      <li>{{ comment.content }}</li>
      <br>

      <button v-if="authStore.isAuthenticated && authStore.userData.username === comment.user.username" @click="commentUpdate(comment.id)">댓글 수정</button> 
      <button v-if="authStore.isAuthenticated && authStore.userData.username === comment.user.username" @click="commentDelete(comment.id)">댓글 삭제</button> 

    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth.js';
import { usePostStore } from '@/stores/post';
import { useRouter } from 'vue-router';


const router = useRouter()
const authStore = useAuthStore();
const postStore = usePostStore();
const postId = router.currentRoute.value.params.postId;

postStore.commentList(postId)

const commentUpdate = (commentId) => {
  router.push({ name: 'commentupdate', params: { commentId: commentId } });
}

const commentDelete = (commentId) => {
  postStore.commentDelete(postId, commentId)
}


</script>
