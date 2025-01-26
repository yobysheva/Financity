<script setup>
import {defineProps, defineEmits, onMounted, onUnmounted, defineExpose, computed} from 'vue';
import {ref} from 'vue';
import {authService} from "@/services/auth";
import store from "@/store";

const emit = defineEmits(['close', 'update-balance', 'plus', 'minus']);
const answerText = ref("Ваше действие будет иметь последствия");

const close = () => {
  emit('close');
  answerTextVisible.value = false;
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

let answerTextVisible = ref(false);

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

let stopAnswering = ref(false)
let didIVote = ref(false)
let timeBeforeClose = ref(10)
let answers = ref([])
let votes_pluses = ref(0)
let votes_minuses = ref(0)

function update_variables() {
    didIVote.value = false
    stopAnswering.value = false
    timeBeforeClose.value = 10
}
function vote_minus() {
    if (stopAnswering.value && !didIVote.value) {
        votes_minuses.value++
        didIVote.value = true
        emit('minus')
        console.log("я проголосовал за минус", didIVote.value)
    }
}

function vote_plus() {
    if (stopAnswering.value && !didIVote.value) {
        didIVote.value = true
        emit('plus')
        console.log("я проголосовал за плюс", didIVote.value)
    }
}

function get_votes() {
    return {
        "pluses": votes_pluses.value,
        "minuses": votes_minuses.value
    }
}

function get_stop_answering() {
    return stopAnswering.value
}

function set_stop_answering(value) {
    console.log(didIVote.value || !value, value)
    stopAnswering.value = value
}


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
    for(let i = 0; i < rates.length; i++){
        if(rates[i].checked){
            return i
        }
    }
    return -1
}

function setTimerThenClose() {
    console.log(didIVote.value)
    stopAnswering.value = true
    if (timeBeforeClose.value > 0) {
        console.log(`${timeBeforeClose.value--} осталось`)
        setTimeout(setTimerThenClose, 1000)
    }
    else {
        stopAnswering.value = false
        timeBeforeClose.value = 10
        close()
    }
}

async function addAnswer() {
  let rates = document.getElementsByName('answer');
  for (let ans of rates) {
    if (ans.checked) {
      let answerId = ans.value;
      let response = await authService.addActionAnswer(store.state.playerID, answerId);
      answerText.value = response.data['text'];
      answerTextVisible.value = true;
      let newBalance = response.data['balance'];
      emit('update-balance', newBalance, store.state.playerID);
    }
  }
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
    if(type === 3){
      const response = await authService.getChance(id);
      question.value.text = response.data['text'];
      return;
    }
    const response = await authService.getQuestion(id);
    question.value.text = response.data['text'];
    // question.value.type = response.data['type'];
    if(type === 2){
      const response1 = await authService.getAnswers(id);
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
    setActiveRadioButtonForId ,
    get_votes,
    get_stop_answering,
    set_stop_answering,
    update_variables
});
</script>

<template>
  <div v-if="visible && !answerTextVisible" class="modal" :style="modalStyles">
    <div class="container modal-container" :style="containerStyles">
      <div class="column" :style="contentStyles">
        <h1 style="margin-bottom: 16px;">{{ caseTitle }}</h1>
        <h3 style="margin-bottom: 16px;">{{ question.text }}</h3>
        <textarea
          v-if="questionType === 1"
          class="input-custom"
          :disabled="!isMyTurn || stopAnswering"
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
        <button v-if="questionType === 2 && isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="addAnswer"
      >
        Ответить
      </button>
      <button v-if="questionType === 3 && isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="close"
      >
        Закрыть
      </button>
        <div class="row" v-if="questionType === 1 && !isMyTurn">
          <button
        class="button-33"
        role="button"
        :hidden="didIVote || !stopAnswering"
        style="margin-bottom: 16px;"
        @click="vote_plus"
      >
        +
      </button>
              <button
        class="button-33"
        role="button"
        :hidden="didIVote || !stopAnswering"
        style="margin-bottom: 16px;"
        @click="vote_minus"
      >
        -
      </button>
        </div>
        <button v-if="questionType === 1 && isMyTurn && !stopAnswering"
        class="button-33"
        role="button"
        :hidden="stopAnswering"
        style="margin-bottom: 16px;"
        @click="setTimerThenClose"
      >
        Ответить
      </button>
        <h3 v-if="questionType === 1 && stopAnswering">{{timeBeforeClose}}</h3>
</div>
    </div>
  </div>
  <div v-if="visible && answerTextVisible" class="modal" :style="modalStyles">
    <div class="container modal-container" :style="containerStyles">
      <div class="column" style="justify-content: center; align-items: center; padding: 5%;" :style="contentStyles">
        <div v-if="questionType === 2">
          <h1>{{ answerText }}</h1>
        </div>
        <button v-if="isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="close"
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