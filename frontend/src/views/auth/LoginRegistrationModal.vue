<template>
  <div v-if="isRegistrationModalVisible" class="modal" id="registration-modal">
    <div class="modal-content">
      <h2>Войдите или зарегистрируйтесь.</h2>
      <input
          v-model="username"
          class="input-custom"
          type="text"
          placeholder="Введите логин"
          @keydown.enter="register"
      />
      <input
          v-model="password"
          class="input-custom"
          type="password"
          placeholder="Введите пароль"
          @keydown.enter="register"
      />
      <input
          v-model="password2"
          class="input-custom"
          type="password"
          placeholder="Повторите пароль"
          @keydown.enter="register"
      />
      <button class="button-33" @click="register" role="button">Создать аккаунт</button>
      <button class="button-33" @click="openLogin" role="button">У меня уже есть аккаунт</button>
    </div>
  </div>

  <div v-if="isLoginModalVisible" class="modal" id="registration-modal">
    <div class="modal-content">
      <h2>Войдите или зарегистрируйтесь.</h2>
      <input
          v-model="username"
          class="input-custom"
          type="text"
          placeholder="Введите логин"
          @keydown.enter="login"
      />
      <input
          v-model="password"
          class="input-custom"
          type="password"
          placeholder="Введите пароль"
          @keydown.enter="login"
      />
      <button class="button-33" @click="login" role="button">Войти</button>
      <button class="button-33" @click="openRegistration" role="button">Создать новый аккаунт</button>
    </div>
  </div>
  <dialog v-show="!isLandscape" open style="background-color:white">
    <p class="vertical-warning">Пожалуйста, поверните свой дивайс в горизонталбное положение 📱🔄</p>
  </dialog>
</template>

<script>
import {authService} from "@/services/auth";
import store from "../../store.js";
const clickSound = require("../../assets/sound/click.wav");
const hoverSound = require("../../assets/sound/hover2.wav")

export default {
  setup() {
      const clickAudio = new Audio(clickSound);
      const hoverAudio = new Audio(hoverSound)

      const buttonClickSound = () => {
        clickAudio.volume = 0.1
        clickAudio.play()
      }
      const buttonHoverSound = () => {
        hoverAudio.volume = 0.1
        hoverAudio.play()
      }

      return { clickAudio ,hoverAudio, buttonClickSound, buttonHoverSound }
  },
  data() {
    return {
      isRegistrationModalVisible: false,
      isLoginModalVisible: true,
      username: '',
      password: '',
      password2: '',
      isLandscape: (window.innerWidth > window.innerHeight),
    };
  },
  props: {
    userLoggedIn: {
      type: Boolean,
    },
  },
  mounted() {
    window.addEventListener('resize', this.checkOrientation);
    this.checkOrientation();
  },
  methods: {
    sendUsername() {
      store.dispatch("updateUsername", this.username);
    },
    sendSecret() {
      store.dispatch("updateSecret", this.secret)
    },
    openLogin() {
      this.buttonClickSound();
      this.isRegistrationModalVisible = false;
      this.isLoginModalVisible = true;
    },
    openRegistration() {
      this.buttonClickSound();
      this.username = '';
      this.password = '';
      this.isRegistrationModalVisible = true;
      this.isLoginModalVisible = false;
    },
    async login() {
      this.buttonClickSound();
      try {
        const response = await authService.login({
          username: this.username,
          password: this.password,
        });
        if (response.status === 202) {
          this.secret = response.data.secret
          this.sendUsername();
          this.sendSecret();
          this.$router.replace({name: "home"});
          this.username = '';
          this.password = '';
        }
      } catch (error) {
        if (error.response) {
          alert("Login failed: " + error.response.data || "Unknown error");
        } else if (error.request) {
          alert("No response from server. Please try again later.");
        } else {
          alert("Error setting up request: " + error.message);
        }
      }
    },
    checkOrientation() {
      this.isLandscape = window.innerWidth > window.innerHeight;
    },
    async register() {
      this.buttonClickSound();
      if (this.password2 === this.password) {
        if (this.username.length <= 15) {
          try {
            const response = await authService.register({
              username: this.username,
              password: this.password,
            });
            if (response.status === 201) {
              this.openLogin();
              alert("User registered successfully!");
              // this.username = '';
              // this.password = '';
              this.password2 = '';
            }
          } catch (error) {
            if (error.response) {
              alert("Registration failed: " + error.response.data || "Unknown error");
            } else if (error.request) {
              alert("No response from server. Please try again later.");
            } else {
              alert("Error setting up request: " + error.message);
            }
          }
        } else {
          alert("Username too long")
        }
      } else {
        alert("Password must match");
      }
    },
  },
};
</script>

<style scoped>
.modal {
  height: 95%;
}

dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  z-index: 9999;
  border: none;
  padding: 0;
  margin: 0;
}

@media (max-width: 1200px) {
  h2 {
    font-size: 16px;
  }
}

@media (max-width: 900px) {
  h2 {
    font-size: 14px;
  }
}

@media (max-width: 770px) {
  h2 {
    font-size: 12px;
  }
}

.button-33 {
  font-size: 16px;
  margin: 25px 30px;
}

@media (max-width: 1200px) {
  .button-33 {
    margin: 17px 26px;
    padding: 5px 17px;
    font-size: 13px;
  }
}

@media (max-width: 900px) {
  .button-33 {
    margin: 13px 23px;
    padding: 3px 13px;
    font-size: 10px;
  }
}

@media (max-width: 770px) {
  .button-33 {
    margin: 10px 19px;
    padding: 3px 10px;
    font-size: 9px;
  }
}

input {
  margin: 25px 30px;
  padding: 10px 20px;
  font-size: 14px;
}

@media (max-width: 1200px) {
  input {
    margin: 17px 26px;
    padding: 5px 17px;
    font-size: 12px;
  }
}

@media (max-width: 900px) {
  input {
    margin: 13px 23px;
    padding: 3px 13px;
    font-size: 10px;
  }
}

@media (max-width: 770px) {
  input {
    margin: 10px 19px;
    padding: 3px 10px;
    font-size: 9px;
  }
}
</style>
