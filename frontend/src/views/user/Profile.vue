<script setup>
import { authService } from "@/services/auth";
import store from "../../store.js";
import { ref } from 'vue';

let user = ref({
  username: 'имя',
  countGames: 0,
  winGames: 0,
  photo: 0,
  place: 0,
})
const images = ref([
  require('@/assets/av1.png'),
  require('@/assets/av2.png'),
  require('@/assets/av3.png'),
  require('@/assets/av4.png'),
  require('@/assets/av5.png'),
  require('@/assets/av6.png'),
]);


async function getData() {
  try {
    const response = await authService.getData(store.state.username);
    user.value.username = store.state.username;
    user.value.countGames = response.data['countGames'];
    user.value.winGames = response.data['winGames'];
    user.value.photo = images.value[response.data['indexPhoto']] || images.value[0];
    user.value.place = response.data['place'];
    await store.dispatch('updatePhoto', response.data['indexPhoto'] || 0);
  } catch (error) {
        console.error(error);
  }
}

async function changePhoto() {
  await store.dispatch('updatePhoto', (store.state.photo + 1) % 6);
  await authService.updatePhoto({
    'username': store.state.username,
    'indexPhoto': store.state.photo,
  });
}

getData();
</script>

<template>
  <div class="row">
    <div class="photo">
      <button class="transparent-button" @click="changePhoto"></button>
      <img :src="images[store.state.photo]" alt="User Photo" />
    </div>
    <div class="column pr">
      <p>Имя: {{ user.username }}</p>
      <p>Выиграно игр: {{ user.winGames }}/{{ user.countGames }}</p>
      <p>Место в рейтинге: {{user.place}}</p>
    </div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.photo {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 30px;
  background-color: white;
  border-radius: 10px;
  box-shadow: rgba(44, 187, 99, 0.1) 0 2px 4px, rgba(44, 187, 99, 0.05) 0 1px 2px;
  overflow: hidden;
  padding: 0;
}

.photo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: inherit;
}

.transparent-button {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  cursor: pointer;
  outline: none;
}

.transparent-button:focus-visible {
  outline: none;
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