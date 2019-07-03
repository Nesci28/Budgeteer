<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
    <Hexagon v-if="loading"></Hexagon>
    <div v-if="!loading">
      <div class="budget" style="margin-bottom: 20px;">
        <select
          id="mois"
          style="margin-right:10px;height:20px;font-size: 16px;background-color:transparent;"
          v-model="currentMonth"
        >
          <option v-for="month in months" :key="month">{{month}}</option>
        </select>
        <select
          id="annee"
          style="margin-right:20px;height:20px;font-size: 16px;background-color:transparent;"
          v-model="currentYear"
        >
          <option v-for="year in years" :key="year">{{year}}</option>
        </select>
        <a @click="loadMonth(currentMonth, currentYear)" class="btn btn-primary">Go</a>
      </div>
      <div class="card" style="margin: 5px;">
        <chartjs-line
          v-bind:beginzero="beginZero"
          v-bind:bind="true"
          v-bind:bordercolor="borderColor"
          v-bind:data="data['month']"
          v-bind:datalabel="dataLabel"
          v-bind:labels="labels['month']"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { Hexagon } from 'vue-loading-spinner';

const axios = require('axios');

axios.defaults.withCredentials = true;
axios.defaults.headers = {
  'Content-Type': 'application/json',
};

export default {
  components: {
    Hexagon,
  },
  data() {
    return {
      beginZero: true,
      borderColor: '#4591a8',
      data: {
        month: [],
      },
      dataLabel: 'Fluctuation',
      labels: {
        month: [8, 10, 12, 14, 16],
      },
      currentMonth: null,
      currentYear: null,
      months: [
        'janvier',
        'fevrier',
        'mars',
        'avril',
        'mai',
        'juin',
        'juillet',
        'aout',
        'septembre',
        'octobre',
        'novembre',
        'decembre',
      ],
      years: [],
      history: null,
      budgets: null,
      loading: true,
    };
  },
  methods: {
    getCurrentMonth() {
      const date = new Date();
      this.currentMonthInt = date.getMonth();
      this.currentMonth = this.months[date.getMonth()];
    },
    getCurrentYear() {
      const date = new Date();
      this.currentYear = date.getFullYear();
      for (let i = 0; i < 3; i++) {
        this.years.push((this.currentYear + i).toString());
      }
    },
    async loadMonth(month, year) {
      this.budgets = await axios.post(this.urlBudget, {
        month: this.months.indexOf(month),
        year,
      });
      this.budgets = this.budgets.data.message;
      this.history = this.budgets.tx_month;
      this.data.month = [];
      this.labels.month = [];
      this.renderChart();
    },
    renderChart() {
      Object.keys(this.history).forEach((day) => {
        if (this.history[day].length > 0) {
          var valueToAdd = 0;
          this.history[day].forEach((tx) => {
            if (tx.hasOwnProperty('type')) {
              valueToAdd += tx.value * -1;
            } else {
              valueToAdd += tx.value;
            }
          });
        }
        let sum = day == 1 ? 0 : this.data.month[this.data.month.length - 1];
        if (valueToAdd) sum += valueToAdd;
        this.data.month.push(sum);
        this.labels.month.push(day);
      });
      this.loading = false;
    },
  },
  async mounted() {
    this.urlBudget = '/api/v2/budget';
    this.getCurrentMonth();
    this.getCurrentYear();
    this.budgets = await axios.post(this.urlBudget, {
      month: this.currentMonthInt,
      year: this.currentYear,
    });
    this.budgets = this.budgets.data.message;
    this.history = this.budgets.tx_month;
    this.renderChart();
  },
};
</script>

<style lang="scss">
.chartjs-render-monitor {
  background-color: rgba(255, 255, 255, 0.5);
}
</style>
