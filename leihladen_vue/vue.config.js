const {
  defineConfig
} = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  pwa: {
    manifestOptions: {
      name: "Leihladen",
      short_name: "Leihladen",
      start_url: "./",
      display: "standalone",
      theme_color: "#000000",
      // icons: [{
      //   src: "./favicon.ico",
      // }, ],
    },

    themeColor: "#4DBA87",
    msTileColor: "#000000",
    appleMobileWebAppCapable: "yes",
    appleMobileWebAppStatusBarStyle: "black",
    icons: {
      maskicon: null,
      favicon32: "./favicon32.png",
      favicon16: "./favicon16.png",
      appleTouchIcon: "./apple-touch-icon.png",
      msTileImage: null,
    },

    workboxPluginMode: "GenerateSW",
  },
})