<script setup>

</script>

<template>
<div class="modal" style="top: 35%; width: 60%; min-height: 30%; height: auto; overflow: visible;">
  <div class="container modal-container" style="width: 100%; min-height: 100%; padding: 5%;">
      <h3>Приглашение в игру</h3>
      <div class="row">
      <p>Пользователь User123 приглашает вас присоединиться к игре</p>
    </div>
      <div class="row">
      <button class="button-33" role="button">Принять приглашение</button>
      <button class="button-33" role="button">Отклонить приглашение</button>
      </div>

  </div>
</div>
  <div class="overlay"></div>
</template>

<style scoped>

.modal{
  opacity: 1;
  padding: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.column{
  align-items: center;
  justify-content: space-between;
}

.container{
  opacity: 1;
}
</style>