<template>
  <div>
    <a href="/#/login" class="btn btn-primary">Login</a>
    <a href="/#/signup" class="btn btn-secondary">Signup</a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      login: false,
      signup: false,
      background: null,
      wallpaper1: false,
      wallpaper2: false,
      wallpaper3: false,
      wallpaper4: false,
      wallpaper5: false,
      wallpaper6: false,
      wallpaper7: false,
      loggedIn: ""
    };
  },
  methods: {
    showMenu(which) {
      if (which == "login") {
        this.signup = false;
        this.login = true;
      }
      if (which == "signup") {
        this.signup = true;
        this.login = false;
      }
    }
  },
  mounted() {
    if (!localStorage["background"]) {
      localStorage["background"] = "wallpaper1.jpg";
    }
    this.background = require(`../assets/${localStorage["background"]}`);
    switch (localStorage["background"]) {
      case "wallpaper1.jpg":
        this.wallpaper1 = true;
        break;
      case "wallpaper2.jpg":
        this.wallpaper2 = true;
        break;
      case "wallpaper3.jpg":
        this.wallpaper3 = true;
        break;
      case "wallpaper4.jpg":
        this.wallpaper4 = true;
        break;
      case "wallpaper5.jpg":
        this.wallpaper5 = true;
        break;
      case "wallpaper6.jpg":
        this.wallpaper6 = true;
        break;
      case "wallpaper7.jpg":
        this.wallpaper7 = true;
        break;
    }
  }
};
</script>

<style lang="scss">
@import "../css/style.min.css";
</style>