<script>
import {authService} from "@/services/auth";
import store from "../../store.js";
import {CometChat} from "@cometchat-pro/chat";
// // eslint-disable-next-line vue/no-export-in-script-setup
export default {
  data() {
    return {
      isRegistrationModalVisible: false,
      isLoginModalVisible: true,
      username: '',
      password: '',
      password2: '',
    }
  },
  props: {
    userLoggedIn: {
      type: Boolean
    }
  },
  methods: {
    authLoginUser() {
      this.showSpinner = true;

      CometChat.login(this.username, "127bc8520b38325a216041848a7bba2eaaa850e0").then(
        () => {
          this.showSpinner = false;
        },
        error => {
          this.showSpinner = false;
          console.log("Login failed with error:", error.code);
        }
      );
    },
    sendUsername() {
      store.dispatch("updateUsername", this.username)
    },
    openLogin() {
      this.isRegistrationModalVisible = false;
      this.isLoginModalVisible = true;
    },
    openRegistration() {
      this.username = '';
      this.password = '';
      this.isRegistrationModalVisible = true;
      this.isLoginModalVisible = false;
    },
    async login() {
      try {
        const response = await authService.login( {
          username: this.username,
          password: this.password,
        });
        if (response.status === 202) {
          // this.$emit('login', true);
          this.sendUsername();
          this.$router.push({ name: "home" });
          this.authLoginUser();
          // this.$router.push({ name: "home" });
          this.username = '';
          this.password = '';
        }
      } catch (error) {
        if (error.response) {
            alert("Login failed: " + error.response.data || "Unknown error");
            //ошибки в error.response.data лежат в словаре в виде (поле в котором возникла ошибка : массив ошибок в этом поле)
            //я вывожу этот словарь в терминале, в котором запущен сервер джанго, в момент попытки входа или регистрации
          } else if (error.request) {
            alert("No response from server. Please try again later.");
          } else {
            alert("Error setting up request: " + error.message);
          }
      }

    },
    async register() {
      if (this.password2 === this.password) {
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
            //ошибки в error.response.data лежат в словаре в виде (поле в котором возникла ошибка : массив ошибок в этом поле)
            //я вывожу этот словарь в терминале, в котором запущен сервер джанго, в момент попытки входа или регистрации
          } else if (error.request) {
            alert("No response from server. Please try again later.");
          } else {
            alert("Error setting up request: " + error.message);
          }
        }
      } else {
        alert("Password must match");
      }
    }
  },
}
</script>

<template>

  <div v-if="isRegistrationModalVisible" class="modal" id="registration-modal">
    <div class="modal-content">
      <h2 style="width: 80%; word-break: break-all;">Войдите или зарегистрируйтесь.</h2>
      <input v-model="username" class="input-custom" type="text" placeholder="Введите логин">
      <input v-model="password" class="input-custom" type="password" placeholder="Введите пароль">
      <input v-model="password2" class="input-custom" type="password" placeholder="Повторите пароль">
<!--      <div class="btn btn-block" @click="register"><a>Create account</a></div>-->
<!--      <div class="btn" @click="openLogin"><a>I already have an account</a></div>-->
      <button class="button-33" @click="register" role="button">Создать аккаунт</button>
      <button class="button-33" @click="openLogin" role="button">У меня уже есть аккаунт</button>
    </div>
  </div>

  <div v-if="isLoginModalVisible" class="modal" id="registration-modal">
    <div class="modal-content">
      <h2>Войдите или зарегистрируйтесь.</h2>
      <input v-model="username" class="input-custom" type="text" placeholder="Введите логин">
<!--      <input type="text" name="name" class="question" id="nme" required autocomplete="off" placeholder="Enter Your Name"/>-->
<!--  <label for="nme"><span>What's your name?</span></label>-->
      <input v-model="password" class="input-custom" type="password" placeholder="Введите пароль">
<!--      <div class="btn" @click="login" type="button"><a>Log in</a></div>-->
      <button class="button-33" @click="login" role="button">Войти</button>
      <button class="button-33" @click="openRegistration" role="button">Создать новый аккаунт</button>
<!--      <button class="button-82-pushable" role="button">-->
<!--  <span class="button-82-shadow"></span>-->
<!--  <span class="button-82-edge"></span>-->
<!--  <span class="button-82-front text">-->
<!--    I don`t have an account-->
<!--  </span>-->
<!--</button>-->
<!--      <div class="btn" @click="openRegistration"><a>I don`t have an account</a></div>-->
    </div>
  </div>
<!--    <div class="overlay" id="overlay"></div>-->
</template>

<style scoped>
.modal {
  height: 95%;
  //overflow-y: scroll;
}
</style>