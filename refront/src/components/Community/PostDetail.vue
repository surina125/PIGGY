<template>
  <div class="table-container mt-4 mb-3 community-page">
    <div class="post-container">
      <p class="post-title">{{ postStore.detailInfos.title }}</p>
      <hr>
      <div class="post-content">
        <p v-for="line in formatContent(postStore.detailInfos.content)" :key="line">{{ line }}</p>
      </div>
      <div v-if="authStore.isAuthenticated && postStore.detailInfos.user.username && authStore.userData.username === postStore.detailInfos.user.username">
        <button type="button" class="btn btn-outline-secondary" @click="postUpdate(postStore.detailInfos.id)">게시물 수정</button>
        <button type="button" class="btn btn-outline-secondary" @click="postStore.postDelete(postStore.detailInfos.id)">게시물 삭제</button>
      </div>

      <hr>
      <div v-if="authStore.isAuthenticated">
        <form @submit.prevent="createComment">
          <div class="commentbox">
            <input type="text" id="comment" v-model="commentText" class="form-control" placeholder="댓글을 입력하세요"/>
            <button type="submit" class="btn btn-outline-secondary">작성</button>
          </div>
        </form>
        <hr>
      </div>
      <div>
        <CommentList />
      </div>
      <div style="text-align: center;">
        <button class="btn btn-outline-secondary" @click="goToList">목록</button>
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

const formatContent = (content) => {
  return content.split('\n');
}

onMounted(() => {
  postStore.postDetail(postId);
  postStore.commentList(postId);
});
</script>

<style scoped>
.table-container {
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 70%;
  margin: 0 auto;
}

.post-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
}

.post-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

.post-content {
  font-size: 18px;
  color: #555;
  margin-bottom: 20px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
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

.commentbox {
  display: flex;
  align-items: center;
  justify-content: center;
}

.commentbox .form-control {
  margin-right: 10px;
  flex: 1;
}

.commentbox .btn {
  flex-shrink: 0;
}
</style>
