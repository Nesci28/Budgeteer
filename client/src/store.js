import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    loggedIn: false,
  },
  getters: {
    loggedIn: loggedIn => state.loggedIn,
  },
});
