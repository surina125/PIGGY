<template>
  <div class="container">
    
    <div class="post-container">
      <p class="post-title">{{ postStore.detailInfos.title }}</p>
      <hr>
      <p class="post-content post-preview">{{ postStore.detailInfos.content }}</p>

      <div v-if="authStore.isAuthenticated && authStore.userData.username === postStore.detailInfos.user.username">
        <button type="button" class="btn btn-outline-dark" @click="postUpdate(postStore.detailInfos.id)">게시물 수정</button>
        <button type="button" class="btn btn-outline-dark" @click="postStore.postDelete(postStore.detailInfos.id)">게시물 삭제</button>
      </div>

      <hr>
      <div v-if="authStore.isAuthenticated">
        <form @submit.prevent="createComment">
        <div class="commentbox">
          <input type="text" id="comment" v-model="commentText" class="form-control" placeholder="댓글을 입력하세요" style="margin-right: 10px;"/>
          <button type="submit" class="btn btn-outline-dark">작성</button>
        </div>
        </form>
        <hr>
      </div>
      <div>
        <CommentList />
      </div>
      <div style="text-align: center;">
        <button class="btn btn-outline-dark" @click="goToList">목록</button>
      </div>
      

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { usePostStore } from '@/stores/post';
import CommentList from '@/components/Community/CommentList.vue';

const authStore = useAuthStore();
const postStore = usePostStore();
const router = useRouter();
const commentText = ref("");

const postId = router.currentRoute.value.params.postId;

const postUpdate = (postId) => {
  router.push({ name: 'postupdate', params: { postId: postId } });
}

const createComment = () => {
  postStore.commentCreate(postId, commentText.value);
  commentText.value = "";
}

const goToList = () => {
  router.push({ name: 'community' });
}
onMounted( () => {
  postStore.postDetail(postId);
});
</script>

<style scoped>
.container {
  width: 70%;
  margin: 0 auto;
  padding-top: 20px;
}

h2 {
  margin-bottom: 20px;
}

.post-container {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.post-content {
  font-size: 18px;
  color: #555;
  margin-bottom: 20px;
}

.btn {
  font-size: 16px;
  margin-right: 10px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-outline-dark {
  background-color: transparent;
  color: #333;
  border-color: #333;
}

.commentbox{
  display: flex;
  align-content: center;
  justify-content: center;

}
.post-preview {
  margin-top: 20px;
  white-space: pre-wrap; /* 줄바꿈과 공백을 유지합니다 */
}
</style>
