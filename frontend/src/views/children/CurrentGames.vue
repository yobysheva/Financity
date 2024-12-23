<script setup>

import GameField from "@/views/children/GameField.vue";

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
  max-height: 45vh;
}
</style>