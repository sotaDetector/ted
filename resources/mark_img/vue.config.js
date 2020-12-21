const webpack = require('webpack')

const path = require('path');

module.exports = {
  css: {
    extract: false,
    loaderOptions: {
      less: {
        javascriptEnabled: true
      }
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        "windows.jQuery": 'jquery'
      })
    ],
  },
  publicPath: './', //输出的根路径  默认是/ 如果你的网站是app.com/vue 这更改此配置项
  outputDir: 'ted',
  assetsDir: 'static',
  devServer: {
    proxy: {
      // detail: https://cli.vuejs.org/config/#devserver-proxy
      '/api': {
        // target: `http://192.168.1.67:8100/`,
        target: `http://47.111.130.154:8200/`,
        // target: `http://192.168.1.86:8100/`, // 家伟
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },

}