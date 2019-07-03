<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
    <Hexagon v-if="loading"></Hexagon>
    <div v-if="!loading" class="configBox">
      <div style="height: auto; padding:20px;" class="item">
        <div id="radioBox" style="display: flex;flex-direction: row;flex-wrap: wrap;">
          <div style v-for="title in titles" :key="title">
            <input
              style="margin:5px; margin-left:20px;"
              type="radio"
              :value="title"
              name="title"
              v-model="radioBox"
            />
            <label style="text-transform:capitalize;" :for="title">{{ title }}</label>
          </div>
        </div>
        <datepicker
          id="date"
          v-model="addDate"
          class="fullscreen-when-on-mobile datepicker"
          placeholder="Choisir Date"
        ></datepicker>
        <input
          id="montant"
          style="float: left;"
          type="text"
          placeholder="montant"
          v-model="montant"
        />
        <a @click="add" class="btn btn-primary">Ajouter</a>
      </div>
    </div>
  </div>
</template>

<script>
import { Hexagon } from "vue-loading-spinner";
import Datepicker from "vuejs-datepicker";

const axios = require("axios");

axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};

export default {
  components: {
    Hexagon,
    Datepicker
  },
  data() {
    return {
      urlConfig: null,
      urlAddTx: null,
      loading: true,
      titles: [],
      addDate: null,
      radioBox: null,
      montant: null
    };
  },
  methods: {
    async add() {
      const radioBoxElement = document.getElementById("radioBox");
      const dateElement = document.getElementById("date");
      const montantElement = document.getElementById("montant");
      radioBoxElement.style.border = "none";
      dateElement.style.border = "none";
      montantElement.style.border = "none";
      if (!this.radioBox) radioBoxElement.style.border = "1px solid red";
      if (!this.addDate) dateElement.style.border = "1px solid red";
      if (!this.montant) montantElement.style.border = "1px solid red";
      if (this.radioBox && this.addDate && this.montant) {
        const year = this.addDate.getFullYear();
        const month = this.addDate.getMonth();
        const day = this.addDate.getDate();
        let res = await axios.post(this.urlAddTx, {
          year,
          month,
          day,
          title: this.radioBox,
          value: this.montant
        });
        res = res.data.message;
        if (res == "tx added") {
          this.titre = "";
          this.addDate = "";
          this.montant = "";
          this.radioBox = false;
        }
      }
    }
  },
  async mounted() {
    this.urlConfig = "/api/v2/getType";
    this.urlAddTx = "/api/v2/addTx";
    this.titles = await axios.get(this.urlConfig);
    this.titles = this.titles.data.message;
    console.log(this.titles);
    this.loading = false;
  },
  created() {
    window.addEventListener("keypress", e => {
      if (e.keyCode == 13) this.add();
    });
  }
};
</script>

<style lang="scss">
</style>
