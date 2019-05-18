import Vue from "vue";
import Router from "vue-router";
import home from "./views/home";
import login from "./views/login";
import signup from "./views/signup";
import settings from "./views/settings";
import account from "./views/account";
import incomeConfig from "./views/incomeConfig";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/income/config",
      name: "incomeConfig",
      component: incomeConfig
    },
    {
      path: "/",
      name: "home",
      component: home
    },
    {
      path: "/login",
      name: "login",
      component: login
    },
    {
      path: "/signup",
      name: "signup",
      component: signup
    },
    {
      path: "/settings",
      name: "settings",
      component: settings
    },
    {
      path: "/account",
      name: "account",
      component: account
    }
  ]
});
