<template>
  <div>
    <p>제목: {{ postStore.detailInfo.title }}</p>
    <p>내용 : {{ postStore.detailInfo.content }}</p>
    
    <button v-if="authStore.userData.username === postStore.detailInfo.user.username" @click="postUpdate(postStore.detailInfo.id)">게시물 수정</button> 
    <button v-if="authStore.userData.username === postStore.detailInfo.user.username" @click="postStore.postDelete(postStore.detailInfo.id)">게시물 삭제</button> 
    <CommentCreate v-if="authStore.isAuthenticated" @comment-submitted="handleComment" />

  </div>
</template>

<script setup>

import { useAuthStore } from '@/stores/auth.js';
import { usePostStore } from '@/stores/post';
import { useRouter } from 'vue-router';
import CommentCreate from '@/components/Community/CommentCreate.vue'


const authStore = useAuthStore()
const postStore = usePostStore()
const router = useRouter()

postStore.postDetail()

const postUpdate = (pk) => {
  router.push({name:'postupdate', params:{postId:pk}})
}

function handleComment(commentText) {
  // 여기에서 댓글 제출
  // console.log('Comment submitted:', commentText);
}
</script>

<style lang="scss" scoped>

</style>