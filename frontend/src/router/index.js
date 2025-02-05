import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/auth/LoginRegistrationModal.vue';
// import {authService} from "@/services/auth";
// import Profile from '../views/Profile.vue';
import Home from '../views/Home.vue';
import Game from '../views/Game.vue'

const routes = [
  {
    path: '/',
    redirect: 'login',
    name: 'homepage'
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
      meta: {
      source: "router"
    }
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: {
      source: "home"
    }
  },
  {
    path: '/game',
    name: 'Game',
    component: Game,
    meta: {
      source: "game"
    },
    props: (route) => ({ id: route.query.id})
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.source === 'game') {
        if (!JSON.parse(sessionStorage.getItem('store_state'))['gameID']){
      next({
        path: '/home',
      })
      return
    }
  }
  next();
});

export default router;