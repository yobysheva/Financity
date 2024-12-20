<script setup>

import RatingUser from "@/views/user/RatingUser.vue";
</script>

<template>
  <div class="container rating">
    <h3>Рейтинг</h3>
    <RatingUser/>
    <RatingUser/>
    <RatingUser/>
    <RatingUser/>
    <RatingUser/>
    <RatingUser/>
    <RatingUser/>
    <RatingUser/>
  </div>
</template>

<style scoped>
.rating{
  overflow-y: scroll;
  height: 70vh;
  position: relative;
}
</style>