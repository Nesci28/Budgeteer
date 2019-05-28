<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
    <Hexagon v-if="loading"></Hexagon>
    <div v-if="!loading" class="configBox">
      <div style="height: 165px; width: 200px;padding:20px;" class="item">
        <input id="titre" style="width: 150px;" type="text" placeholder="Titre" v-model="titre">
        <datepicker
          id="date"
          v-model="addDate"
          class="fullscreen-when-on-mobile"
          placeholder="Choisir Date"
        ></datepicker>
        <input
          id="montant"
          style="margin-top: 10px;width: 150px;"
          type="text"
          placeholder="Montant"
          v-model="montant"
        >
        <a
          @click="add"
          style="position: absolute;left: 40px;top: 142px;"
          class="btn btn-primary"
        >Ajouter</a>
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
      urlConfig: null,
      urlAddTx: null,
      loading: true,
      addDate: null,
      montant: null,
      titre: null
    };
  },
  methods: {
    async add() {
      const titreBoxElement = document.getElementById("titre");
      const dateElement = document.getElementById("date");
      const montantElement = document.getElementById("montant");
      titreBoxElement.style.border = "none";
      dateElement.style.border = "none";
      montantElement.style.border = "none";
      if (!this.titre) titreBoxElement.style.border = "1px solid red";
      if (!this.addDate) dateElement.style.border = "1px solid red";
      if (!this.montant) montantElement.style.border = "1px solid red";
      if (this.titre && this.addDate && this.montant) {
        const year = this.addDate.getFullYear();
        const month = this.addDate.getMonth();
        const day = this.addDate.getDate();
        let res = await axios.post(this.urlAddTx, {
          year,
          month,
          day,
          title: this.titre,
          value: this.montant
        });
        res = res.data.message;
        if (res == "tx added") {
          this.titre = "";
          this.addDate = "";
          this.montant = "";
        }
      }
    }
  },
  async mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlAddTx = "http://localhost:5000/addTx";
    } else if (window.location.href.includes("192.168")) {
      this.urlAddTx = "http://192.168.0.127:5000/addTx";
    } else {
      this.urlAddTx = "https://budgeteer-server.now.sh/addTx";
    }
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
#date {
  margin-top: 10px;
  width: 150px !important;
}
</style>