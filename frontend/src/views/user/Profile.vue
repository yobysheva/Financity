<script setup>
import { authService } from "@/services/auth";
import store from "../../store.js";
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['updatePhoto'])

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
  emit('updatePhoto')
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

.photo{
  position: relative;
  width: 150px;
  height: 150px;
  margin: 30px;
  @media(max-width: 1200px) {
    width: 120px;
    height: 120px;
    margin: 25px;
  }
  @media(max-width: 900px) {
    width: 100px;
    height: 100px;
    margin: 20px;
  }
  @media(max-width: 770px) {
    width: 75px;
    height: 75px;
    margin: 16px;
  }
  background-color: white;
  border-radius: 10px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  /*font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;*/
  padding: 0;
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

.photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  @media(max-width: 1200px) {
    font-size: 10px;
  }
  @media(max-width: 900px) {
    font-size: 8px;
  }
  @media(max-width: 770px) {
    font-size: 6px;
  }
  font-weight: bold;
}

.pr{
  font-weight: bold;
  text-align: left;
  justify-content: center;
}
</style>