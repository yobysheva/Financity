<script setup>
import RatingUser from "@/views/user/RatingUser.vue";
</script>

<template>
  <h3>Присоединись к этим играм!</h3>
<div class="container games">
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
.games{
  overflow-y: scroll;
  height: 40vh;
}
</style>