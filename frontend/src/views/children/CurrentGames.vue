<script setup>

import GameField from "@/views/children/GameField.vue";

</script>

<template>
<div class="container games">
  <div v-for="game in this.activeGame"
       :key="game.game_id">
    <div class="row">
      <p>1</p>
      <div class="photo"></div>
      <p>{{ game.username }}</p>
      <p>Создана игра: {{game.game_id}}</p>
    </div>
  </div>
</div>
</template>

<style scoped>
.games{
  overflow-y: scroll;
  max-height: 45vh;
}
</style>