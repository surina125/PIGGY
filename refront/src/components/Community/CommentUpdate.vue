<template>
  <div>
    <h3>댓글 수정</h3>
    <form @submit.prevent="handleSubmitComment">
      <label for="content">댓글:</label>
      <input type="text" id="content" v-model="content"/>

      <button type="submit">commit</button>
    </form>
 
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'


const postStore = usePostStore()
const content = ref('')
const router = useRouter()

const commentId = router.currentRoute.value.params.commentId;

function handleSubmitComment() {
  const updateData = {
    content: content.value
  };
 
  postStore.commentUpdate(postStore.detailInfos.id, commentId, updateData)
  .then(() => {
    router.push({
      name: 'postdetail',
      params: { postId: postStore.detailInfos.id }
    });
  })
  .catch((error) => {
    console.error(error);
  });
}

</script>

<style lang="scss" scoped>

</style>