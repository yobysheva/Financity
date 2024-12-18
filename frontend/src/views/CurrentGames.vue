<script setup>

import GameField from "@/views/GameField.vue";
</script>

<template>
<div class="container games">
  <GameField/>
  <GameField/>
  <GameField/>
  <GameField/>
  <GameField/>
  <GameField/>
  <GameField/>
  <GameField/>
</div>
</template>

<style scoped>
.games{
  overflow-y: scroll;
  max-height: 40vh;
}
</style>