<template>
  <div class="calendar">
    <vue-cal
      :selected-date="selectedDate"
      :disable-views="['years', 'year', 'week', 'day']"
      default-view="month"
      :events-on-month-view="true"
      :events="events"
      style
      class="vuecal--blue-theme"
    ></vue-cal>
  </div>
</template>

<script>
import VueCal from "vue-cal";
import "vue-cal/dist/vuecal.css";

export default {
  components: { VueCal },
  data() {
    return {
      selectedDate: this.getDate(),
      events: [
        {
          start: "2019-05-17",
          end: "2019-05-17",
          title: "Assurance auto",
          content: "100.25",
          class: "outcome"
        },
        {
          start: "2019-05-17",
          end: "2019-05-17",
          title: "Paie",
          content: "1950.33",
          class: "income"
        }
      ]
    };
  },
  methods: {
    getDate() {
      const today = new Date();
      const date =
        today.getFullYear() +
        "-" +
        (today.getMonth() + 1) +
        "-" +
        today.getDate();
    }
  }
};
</script>

<style lang='scss'>
</style>