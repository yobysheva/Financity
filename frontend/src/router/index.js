import { createRouter, createWebHistory } from 'vue-router';
import HomeComet from '../views/HomeComet.vue';
import Login from '../views/auth/LoginRegistrationModal.vue';
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
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
  },
  {
    path: '/comet',
    name: 'comet',
    component: HomeComet
  },
  {
    path: '/game',
    name: 'Game',
    component: Game,
    props: (route) => ({ id: route.query.id})
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;