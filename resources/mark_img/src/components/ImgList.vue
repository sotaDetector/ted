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
        <li :class="{'actived': idx==activeIdx}" @click="chooseImg(item,idx)" v-for="(item,idx) in imgList" :key="idx">
          <img :src="item.ditFilePath" alt="" />
          <Icon type="md-close-circle" class="del" v-if="idx!=activeIdx" @click.stop.prevent="delImg(item._id)" />
        </li>
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
      total: 0,// 初始化信息总条数
      pageNow: 1,
      pagesize: 20,// 每页显示多少条
      imgList: [
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (3).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (3).jpg"),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (2).jpg"),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require('@/assets/img/美女.jpg'),
        // require("@/assets/img/timg (1).jpg"),
        // require("@/assets/img/timg (2).jpg"),
        // require("@/assets/img/timg (1).jpg"),
        // require("@/assets/img/timg (3).jpg"),
        // require("@/assets/img/timg (3).jpg"),
        // require("@/assets/img/white.jpg"),
        // require("@/assets/img/timg (2).jpg"),
      ]
    }
  },
  mounted () {
    this.getImgs()
  },
  methods: {
    getImgs () {
      var id = this.$route.params.id
      let params = {
        pageSize: this.pagesize,
        pageIndex: this.pageNow,
        dsId: parseInt(id)
      }
      this.$Spin.show()
      this.$post('/dsc/getImageItemList', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.imgList = data.pageData.dataList;
          this.total = data.pageData.totalPages;//总数
          this.chosePage = data.pageData.page;//选择页
          this.pageNow = data.pageData.page;//当前页

          setTimeout(() => {
            $('.list').width($('.list li').length * 80)
            this.listWidth = $('.list').width()
            this.boxWidth = $('.img_list').width()
            var index = 0
            var ditId = this.$route.params.ditId
            if(ditId) {
              this.activeIdx = index = this.imgList.findIndex(item => item._id == ditId)
            }
            var index = this.imgList[this.activeIdx] ? this.activeIdx : 0
            this.chooseImg(this.imgList[index], this.activeIdx)
          }, 200);
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    delImg (id) {
      this.$Spin.show()
      this.$post('/dsc/delImageItem', { ditId: id }).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.$Message.success('删除成功')
          this.getImgs()
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    chooseImg (item, idx) {
      this.activeIdx = idx
      this.$emit('chooseImg', item)
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
  padding: 10px 60px 0;
}
.img_list {
  width: calc(100% - 40px);
  margin: 0 auto;
  overflow: hidden;
  position: relative;
  height: 70px;
  padding-top: 10px;
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
  position: relative;
  &.actived {
    border: 2px solid rgb(94, 207, 66);
  }
  img {
    width: 100%;
    height: 100%;
  }
  .del {
    color: #ff2842;
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 18px;
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
  top: 20px;
}
.left {
  left: 0;
}
.right {
  right: 0;
}
</style>