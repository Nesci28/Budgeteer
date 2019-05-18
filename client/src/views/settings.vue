<template>
  <div>
    <img
      v-for="image in images"
      :key="image.url"
      :src="image.url"
      :id="image.id"
      height="100px"
      width="auto"
      class="backgroundThumbnail"
      @click="changeSelection(image)"
      v-bind:class="{'backgroundThumbnailActive': checkActiveWallpaper(image.url)}"
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [
        { url: require("../assets/wallpaper1.jpg"), id: "wallpaper1" },
        { url: require("../assets/wallpaper2.jpg"), id: "wallpaper2" },
        { url: require("../assets/wallpaper3.jpg"), id: "wallpaper3" },
        { url: require("../assets/wallpaper4.jpg"), id: "wallpaper4" },
        { url: require("../assets/wallpaper5.jpg"), id: "wallpaper5" },
        { url: require("../assets/wallpaper6.jpg"), id: "wallpaper6" },
        { url: require("../assets/wallpaper7.jpg"), id: "wallpaper7" }
      ],
      background: localStorage["background"]
    };
  },
  methods: {
    checkActiveWallpaper(image) {
      const activedWallpaper = localStorage["background"];
      image = image.split(".")[0].split("/")[2];
      if (activedWallpaper.includes(image)) return true;
      return false;
    },
    changeSelection(image) {
      const id = image.id;

      const oldBackgroundElement = document.getElementById(
        localStorage["background"].split(".")[0]
      );
      oldBackgroundElement.classList.remove("backgroundThumbnailActive");

      const newBackgroundelement = document.getElementById(id);
      newBackgroundelement.classList.add("backgroundThumbnailActive");

      image.url.split(".")[0].split("/")[2];
      localStorage["background"] = image.id + ".jpg";

      this.background = require(`../assets/${localStorage["background"]}`);
      const backgoungElement = document.getElementById("app");
      backgoungElement.style.background = `url(${
        this.background
      }) no-repeat center center/cover`;
    }
  }
};
</script>

<style lang="scss">
</style>