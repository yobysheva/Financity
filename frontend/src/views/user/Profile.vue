<script setup>
import { authService } from "@/services/auth";
import store from "../../store.js";
import { ref } from 'vue';

let user = ref({
  username: 'имя',
  countGames: 0,
  winGames: 0,
})


async function getData() {
  try {
    console.log(store.state.username);
    const response = await authService.getData(store.state.username);
    console.log(response);
    user.value.username = store.state.username;
    user.value.countGames = response.data['countGames'];
    user.value.winGames = response.data['winGames'];
  } catch (error) {
        console.error(error);
  }
}

getData();
</script>

<template>
<!--<div class="modal">-->
<!--  <div class="modal-content column">-->
    <div class="row">
      <div class="photo"></div>
      <div class="column pr">
        <p>Имя: {{ user.username }}</p>
        <p>Выиграно игр: {{ user.winGames }}/{{ user.countGames }}</p>
        <p>Место в рейтинге: 5/187</p>
      </div>
    </div>
<!--  </div>-->

<!--</div>-->
<!--  <div class="overlay"></div>-->
</template>

<style scoped>
.row{
  height: 20%;
}

.photo{
  width: 150px;
  height: 150px;
  margin: 30px;
  background-color: white;
  border-radius: 10px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  /*font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;*/
  padding: 10px 15px;
  font-size: 16px;
  border: 2px solid rgba(44, 187, 99, .3);
  transition: all 250ms;
}

.photo:focus {
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

.photo::placeholder {
  color: #aaa;
  opacity: 0.8;
}

.photo:hover {
  //background-color: rgba(100, 255, 200, .9);
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

p{
  font-size: 14px;
  font-weight: bold;
}

.pr{
  font-weight: bold;
  text-align: left;
  justify-content: center;
}

</style>