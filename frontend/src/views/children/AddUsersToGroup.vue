<script setup>
import { ref } from 'vue';
const props = defineProps({
  gameId: String
})

let groupUsers = ref([])

function addUserToGroup(username){

}


</script>

<template>
<div class="modal" style="top: 35%; width: 50%; min-height: 40%; height: auto;overflow: visible;">
  <div class="container modal-container" style="width: 100%; min-height: 100%; ">
    <div class="column">
      <div class="row">
      <div class="photo"></div>
      <h3 style="width: 400px;">Вы пригласили в игру:</h3>
        <div class="column">
          <p v-for="user in groupUsers">{{user}}</p>
        </div>
    </div>
      <textarea class="input-custom" style="min-height: 20%; width: 400px;" placeholder="Введите уникальный id пользователей, которых хотите пригласить в игру"></textarea>
    </div>
  </div>
</div>
  <div class="overlay"></div>
</template>

<style scoped>

.modal{
  opacity: 0.9;
  padding: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.column{
  align-items: center;
  justify-content: center;
}

.container{
  opacity: 1;
}


</style>