<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
    <Hexagon v-if="loading"></Hexagon>
    <div class="configBox">
      <div class="item">
        <div style="float: left;" v-for="title in titles" :key="title">
          <input type="radio" id="one">
          <label for="one">{{ title }}</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");
axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};
import { Hexagon } from "vue-loading-spinner";
import Datepicker from "vuejs-datepicker";

export default {
  components: {
    Hexagon,
    Datepicker
  },
  data() {
    return {
      loading: true,
      titles: []
    };
  },
  methods: {},
  async mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlConfig = "http://localhost:5000/getType";
    } else if (window.location.href.includes("192.168")) {
      this.urlConfig = "http://192.168.0.127:5000/getType";
    } else {
      this.urlConfig = "https://nos-server.now.sh/getType";
    }
    this.titles = await axios.get(this.urlConfig);
    this.titles = this.titles.data.message;
    console.log(this.titles);
    this.loading = false;
  }
};
</script>

<style lang="scss">
</style>