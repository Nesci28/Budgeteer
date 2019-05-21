<template>
  <div>
    <a style="margin-right: 20px;" href="/#/login" class="btn btn-primary">Login</a>
    <a href="/#/signup" class="btn btn-secondary">Signup</a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loggedIn: ""
    };
  },
  methods: {},
  mounted() {
    if (!localStorage["background"]) {
      localStorage["background"] = "wallpaper1.jpg";
    }
  }
};
</script>

<style lang="scss">
</style>