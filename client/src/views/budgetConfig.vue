<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
    <Hexagon v-if="loading"></Hexagon>
    <div v-if="!loading" class="budgetBox">
      <div class="budgetItem" v-for="(budget, index) in budgets" :key="budget.title">
        <h3>{{budget.title}}</h3>
        <input type="text" placeholder="montant" v-model="budget.value">
        <div style="margin-top: 10px;">
          <a @click="save(index, budget.title, budget.value)" class="btn btn-primary">Save</a>
          <a @click="remove(index)" class="btn btn-danger">Del</a>
        </div>
      </div>
      <div id="addForm" class="budgetItem">
        <div>
          <input
            id="title"
            type="text"
            placeholder="titre"
            v-model="titre"
            style="width:90%;margin-top: 2px;margin-bottom: 0px;"
          >
        </div>
        <div>
          <input
            id="value"
            type="text"
            placeholder="montant"
            v-model="montant"
            style="margin-bottom: 5px;"
          >
        </div>
        <div style="margin-top: 10px;">
          <a @click="add(titre, montant)" class="btn btn-success">+</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Hexagon } from "vue-loading-spinner";
const axios = require("axios");
axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};

export default {
  components: {
    Hexagon
  },
  data() {
    return {
      loading: true,
      urlBudget: "",
      budgets: null,
      titre: null,
      montant: null
    };
  },
  methods: {
    async save(index, title, value) {
      this.budgets[index].value = parseFloat(value);
      axios.post(this.urlBudget, {
        type: "budget_save",
        index,
        value
      });
    },
    async remove(index) {
      this.budgets.splice(index, 1);
      axios.post(this.urlBudget, {
        type: "budget_remove",
        index
      });
    },
    async add(title, value) {
      const titleElement = document.getElementById("title");
      const valueElement = document.getElementById("value");
      const addFormElement = document.getElementById("addForm");
      if (title && value) {
        const response = await axios.post(this.urlBudget, {
          type: "budget_add",
          title,
          value
        });
        titleElement.style.border = "none";
        valueElement.style.border = "none";
        if (response.data.message != "category already exist") {
          addFormElement.style.border = "solid 3px black";
          this.budgets.push({ title, value });
          this.titre = "";
          this.montant = "";
        } else {
          addFormElement.style.border = "solid 3px red";
        }
      } else {
        if (!titleElement.value) titleElement.style.border = "1px solid red";
        else titleElement.style.border = "none";
        if (!valueElement.value) valueElement.style.border = "1px solid red";
        else valueElement.style.border = "none";
      }
    }
  },
  async mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlBudget = "http://localhost:5000/config/budget";
    } else if (window.location.href.includes("192.168")) {
      this.urlBudget = "http://192.168.0.127:5000/config/budget";
    } else {
      this.urlBudget = "https://nos-server.now.sh/config/budget";
    }
    this.budgets = await axios.get(this.urlBudget);
    this.budgets = this.budgets.data.message;
    this.loading = false;
  }
};
</script>

<style lang='scss'>
</style>