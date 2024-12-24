<script setup>
import { defineEmits, onMounted, onUnmounted } from 'vue';

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};

const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    close();
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
<div class="modal" style="top: 35%; width: 70%;  min-height: 80%; overflow: visible;">
  <div class="container modal-container" style="width: 100%; min-height: 100%; padding: 20px; overflow: auto;-ms-overflow-style: none;
      scrollbar-width: none;">
    <div class="column">
      <p>Правила игры:</p>
      <p>Перед началом игрокам в случайном порядке распределяются профессии с заработной платой (каждый круг, проходя через клетку старт, игрокам начисляется соответствующая сумма на игровой счет).</p>
      <p>Фишки игроков появляются на клетке старт и начинается игра.</p>
      <p>Попадая на определенную зону, игрок решает кейс (в развернутом или тестовом варианте).</p>
      <p>Развернутый вариант: игрок диктует или пишет в чате свой вариант решения проблемы, после у других игроков появляется возможность оценить ответ. После голосования, отвечающему начисляют сумму денег соответствующую количеству игроков проголосовавших положительно.</p>
      <p>Тестовый вариант:</p>
      <p>Игроки выбирают один из представленных вариантов ответов в соответствии со своим бюджетом и своими возможностями. Каждый вариант ответа имеет либо немедленные последствия для игрока (например списание или начисление суммы), либо будущие последствия (суммы будут списывать или начислять каждый круг, также возможен пропуск хода).</p>
      <p>Игра заканчивается, когда кто-либо из игроков становится банкротом или все участники захотят завершить игру. В конце происходить подсчёт капитала каждого игрока, победителем считается тот, у кого на счету осталось больше всего денег.</p>
       <button class="button-33" role="button" @click="emit('close')">Закрыть</button>
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
  text-align: center;
}

.container{
  opacity: 1;
}

</style>