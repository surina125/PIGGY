import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from './auth'

export const usePostStore = defineStore('post', () => {


  const route = useRoute()
  const router = useRouter()
  const authStore = useAuthStore()
  const postInfos = ref([])
  const detailInfo = ref({})

  const postList = function() {
    axios.get('http://127.0.0.1:8000/community/post/')
    .then(response => {
      postInfos.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
    
  }

  const postDetail = function () {
    axios({
      method:'get',
      url:`http://127.0.0.1:8000/community/post/${route.params.postId}/`,
    })
    .then((response) => {
      console.log(response.data)
      detailInfo.value = response.data
      
    })
    .catch((error)=>{
      console.log(error)
    })
  
  }
 const updatePostId = ref('') 

const postUpdate = function(update) {
  return axios({
    method : 'put',
    url : `http://127.0.0.1:8000/community/post/${route.params.postId}/edit/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
    data : {
      title: update.title,
      content: update.content
    }
  })
  .then((response) => {
    updatePostId.value = response.data.id;
    return response.data;
  })
  .catch((error) => {
    console.log(error);
    throw error;
  });
};


 const postDelete = function(postId) {
  axios({
    method:'delete',
    url:`http://127.0.0.1:8000/community/post/${postId}/edit/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    },
  })
  .then((response) => {
    router.push({name:'community'})
    
  })
  .catch((error)=>{
    console.log(error)
  })

}

const commentCreate = function() {

}


 
 return { route, postInfos, detailInfo, postList, postDetail, updatePostId, postUpdate, postDelete, commentCreate}
}, { persist: true })
