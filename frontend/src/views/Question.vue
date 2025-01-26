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
  isMyTurn: Boolean
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

function setTextInTextArea(text) {
  const textarea = document.querySelector('.input-custom');
  textarea.value = text
}

function getTextInTextArea() {
  return document.querySelector('.input-custom').value
}

function getIdOfActiveRadioButton() {
    let rates = document.getElementsByName('answer');
    console.log(rates)
    for(let i = 0; i < rates.length; i++){
        console.log(rates[i].checked)
        if(rates[i].checked){
            return i
        }
    }
    return -1
}

function setActiveRadioButtonForId(id) {
    let rates = document.getElementsByName('answer');
        for(let i = 0; i < rates.length; i++){
            rates[i].checked = false
        }
        if (Number(id) !== -1) rates[id].checked = true
  }

async function getQuestion(id, type) {
  try {
    console.log(store.state.username);
    if(type === 3){
      console.log(1);
      const response = await authService.getChance(id);
      console.log("3. ", response);
      console.log(props);
      question.value.text = response.data['text'];
      return;
    }
    console.log(2);
    const response = await authService.getQuestion(id);
    console.log("3. ", response);
    console.log(props);
    question.value.text = response.data['text'];
    // question.value.type = response.data['type'];
    if(type === 2){
      console.log(3);
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

defineExpose({
    getQuestion ,
    setTextInTextArea ,
    getTextInTextArea ,
    getIdOfActiveRadioButton ,
    setActiveRadioButtonForId
});
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
          :disabled="!isMyTurn"
          style="min-height: 120px; height:40%; width: 100%; padding: 40px; margin-bottom: 16px;"
        ></textarea>
        <div v-if="questionType === 2" class="answers" style="justify-content: space-between;">
          <div
            class="radio-container column"
            style="margin-bottom: 8px; align-items: center; -ms-overflow-style: none; scrollbar-width: none;"
          >
            <label v-for="answer in answers"
            :key="answer.id" style="color:black; display: flex; align-items: center;">
              <input type="radio" name="answer" :value="answer.id" :disabled="!isMyTurn" />
              <div class="radio-custom"></div>
              {{ answer.text }}
            </label>
          </div>
        </div>

      <button v-if="questionType !== 1 && isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="$emit('close')"
      >
        Закрыть
      </button>
        <div class="row" v-if="questionType === 1">
          <button
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="$emit('close')"
      >
        +
      </button>
              <button
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="$emit('close')"
      >
        -
      </button>
        </div>

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

input[type="radio"] {
    display: none;
}

.radio-container {
    display: flex;
    align-items: center;
    margin: 10px 0;
    cursor: pointer;
}

.radio-custom {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(44, 187, 99, .6);
    border-radius: 10px;
    position: relative;
    margin-right: 10px;
    transition: background-color 0.3s, border-color 0.3s;
    flex-shrink: 0;
}

input[type="radio"]:checked + .radio-custom {
    background-color: rgba(44, 187, 99, .3);
}

.radio-custom::after {
    content: '';
    width: 5px;
    height: 5px;
    background-color: white;
    border-radius: 10px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    transition: transform 0.3s;
}

input[type="radio"]:checked + .radio-custom::after {
    transform: translate(-50%, -50%) scale(1);
}

/* Стили для кастомного RadioButton при наведении */
.radio-custom:hover {
    border-color: rgba(44, 187, 99, .3); /* Измените цвет границы при наведении */
}

/* Стили для активного состояния при наведении */
input[type="radio"]:checked + .radio-custom:hover {
    background-color: rgba(44, 187, 99, .3); /* Измените цвет фона при наведении на выбранный RadioButton */
}

</style>