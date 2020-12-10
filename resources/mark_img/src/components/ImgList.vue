<template>
  <div class="container">
    <div class="left" @click="clickLeft">
      <Icon type="ios-arrow-back" />
    </div>
    <div class="img_list">
      <!-- <ul class="list">
        <li @click="chooseImg()" v-for="(item,idx) in 15" :key="idx"><img src="@/assets/img/美女.jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/timg (1).jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/timg (2).jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/timg (3).jpg" alt="" /></li>
        <li @click="chooseImg()"><img src="@/assets/img/white.jpg" alt="" /></li>
      </ul> -->
      <ul class="list">
        <li :class="{'actived': idx==activeIdx}" @click="chooseImg(item,idx)" v-for="(item,idx) in imgList" :key="idx"><img :src="item" alt="" /></li>
      </ul>
    </div>
    <div class="right" @click="clickRight">
      <Icon type="ios-arrow-forward" />
    </div>
  </div>
</template>

<script>



export default {
  data () {
    return {
      // left: '',
      activeIdx: 0,
      imgList: [
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (2).jpg"),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (1).jpg"),
        require("@/assets/img/timg (2).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (3).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (2).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (1).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (2).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (1).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (3).jpg"),
        require("@/assets/img/timg (2).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (2).jpg"),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require('@/assets/img/美女.jpg'),
        require("@/assets/img/timg (1).jpg"),
        require("@/assets/img/timg (2).jpg"),
        require("@/assets/img/timg (1).jpg"),
        require("@/assets/img/timg (3).jpg"),
        require("@/assets/img/timg (3).jpg"),
        require("@/assets/img/white.jpg"),
        require("@/assets/img/timg (2).jpg"),
      ]
    }
  },
  mounted () {
    setTimeout(() => {
      $('.list').width($('.list li').length * 80)
      this.listWidth = $('.list').width()
      this.boxWidth = $('.img_list').width()

      this.chooseImg(this.imgList[0], 0)
    }, 200);
  },
  methods: {
    chooseImg(src,idx) {
      this.activeIdx = idx
      this.$emit('chooseImg', src)
    },
    clickLeft () {
      var left = $('.list').position().left
      left += 500
      if(left >= 0) {
        $('.list').animate({ left: 0 })
        return false
      }
      $('.list').animate({ left: left + 'px' })
    },
    clickRight () {
      var left = $('.list').position().left
      left -= 500
      if(left <= this.boxWidth - this.listWidth) {
        $('.list').animate({ left: (this.boxWidth - this.listWidth) + 'px' })
        return false
      }
      $('.list').animate({ left: left + 'px' })
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  width: 100%;
  color: #fff;
  height: 110px;
  position: absolute;
  bottom: 0;
  left: 0;
  padding: 0 60px;
}
.img_list {
  width: calc(100% - 40px);
  margin: 0 auto;
  overflow: hidden;
  position: relative;
}
.list {
  display: flex;
  // justify-content: center;
  // width: calc(100% - 40px);
  position: relative;
  left: 0;
  width: auto;
}
.list li {
  width: 60px;
  height: 60px;
  margin: 0 10px;
  cursor: pointer;
  flex: none;
  &.actived {
    border: 2px solid rgb(94, 207, 66);
  }
  img {
    width: 100%;
    height: 100%;
  }
}
.right,
.left {
  cursor: pointer;
  width: 60px;
  height: 60px;
  color: #fff;
  font-size: 30px;
  line-height: 60px;
  text-align: center;
  background: rgba(255, 255, 255, 0.3);
  position: absolute;
  top: 0;
}
.left {
  left: 0;
}
.right {
  right: 0;
}
</style>