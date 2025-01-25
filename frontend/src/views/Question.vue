<script setup>
import {defineProps, defineEmits, onMounted, onUnmounted, defineExpose, computed} from 'vue';
import store from "@/store";
import {ref} from 'vue';
import {authService} from "@/services/auth";

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

const props = defineProps({
  questionId: Number,
  caseTitle: String,
  questionType: Number,
  // questionText: String,
  visible: Boolean,
  color: String,
});

const modalStyles = computed(() => ({
  top: "35%",
  width: "70%",
  minHeight: "30%",
  maxHeight: "90%",
  height: "80%",
  overflow: "visible",
  position: "fixed",
  left: "50%",
  transform: "translate(-50%, -35%)",
  zIndex: 1000,
  padding: 0,
}));

const containerStyles = computed(() => ({
  backgroundColor: props.color || "white",
  width: "100%",
  height: "100%",
  padding: "16px",
  overflowY: "auto",
 msOverflowStyle: "none",
  scrollbarWidth: "none",
  boxSizing: "border-box",
  position: "relative",
}));

const contentStyles = computed(() => ({
  padding: "16px",
  display: "flex",
  flexDirection: "column",
  justifyContent: "flex-start",
  alignItems: "center",
  gap: "2%",
  width: "100%",
  boxSizing: "border-box",
  position: "relative",
}));


let question = ref({
  text : "",
});

let answers = ref([])

onMounted(() => {
  const textarea = document.querySelector('.input-custom');
  const container = document.querySelector('.modal-container');

  if (textarea && container) {
    textarea.addEventListener('input', function () {
      this.style.height = 'auto'; // Сбрасываем высоту текстового поля
      this.style.height = this.scrollHeight + 'px'; // Устанавливаем высоту равной высоте содержимого

      // Увеличиваем высоту контейнера в зависимости от высоты текстового поля
      container.style.minHeight = this.scrollHeight + 140 + 'px'; // Добавьте отступ для упаковки
    });
  }
});


async function getQuestion(id, type) {
  try {
    console.log(store.state.username);
    if(type === 3){
      const response = await authService.getChance(id);
    console.log("3. ", response);
    console.log(props);
    question.value.text = response.data['text'];
    return;
    }
    const response = await authService.getQuestion(id);
    console.log("3. ", response);
    console.log(props);
    question.value.text = response.data['text'];
    // question.value.type = response.data['type'];
    if(type === 2){
      const response1 = await authService.getAnswers(id);
      console.log("3. ", response1);
      answers.value = [];
      for(const answer of response1.data){
        answers.value.push(answer);
      }
    }
  } catch (error) {
        console.error(error);
  }
}

defineExpose({ getQuestion });
</script>

<template>
  <div v-if="visible" class="modal" :style="modalStyles">
    <div class="container modal-container" :style="containerStyles">
      <div class="column" :style="contentStyles">
        <h3 style="margin-bottom: 16px;">{{ caseTitle }}</h3>
        <h3 style="margin-bottom: 16px;">{{ question.text }}</h3>
        <textarea
          v-if="questionType === 1"
          class="input-custom"
          style="min-height: 120px; height:40%; width: 100%; padding: 25px; margin-bottom: 16px;"
        ></textarea>
        <div v-if="questionType === 2" class="answers">
          <div
            class="column"
            style="margin-bottom: 8px; align-items: center; -ms-overflow-style: none; scrollbar-width: none;"
          >
            <label v-for="answer in answers"
            :key="answer.id" style="color:black; ">
              <input type="radio" name="answer" :value="answer.id" />
              {{ answer.text }}
            </label>
          </div>
        </div>
      <button
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="$emit('close')"
      >
        Закрыть
      </button>
      </div>
    </div>
  </div>
  <div v-if="visible" class="overlay"></div>
</template>

<style scoped>
.photo{
  width: 50px;
  height: 50px;
  margin: 10px;
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

.modal{
  opacity: 0.9;
  padding: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
  max-height: 90vh;
  overflow-y: auto;
}

.column{
  align-items: center;
  justify-content: center;
}

.container{
  opacity: 1;
}

.buttons{
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
}
h3{
  width: 80%;
}
</style>