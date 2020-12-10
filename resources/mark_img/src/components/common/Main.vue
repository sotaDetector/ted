<template>
    <div class="wrapper">
        <v-head></v-head>
        <!-- <v-leftlogo></v-leftlogo> -->
        <v-sidebar></v-sidebar>
        <div class="content-box">
            <div class="content">
                <transition name="move" mode="out-in">
                    <router-view></router-view>
                </transition>
            </div>
        </div>
    </div>
</template>
<script>
import vHead from './Header'
import vLeftlogo from './LeftLogo'
import vSidebar from './SideBar'
export default {
  name: "Main",
  data() {
    return {
    }
  },
  components:{
      vHead,vSidebar,vLeftlogo
  }
}
</script>
<style scoped>
.wrapper{
    width: 100%;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.content-box{
    height: 100%;
    position: absolute;
    left: 200px;
    right: 0;
    top: 40px;
    bottom: 0;
    overflow-y: scroll;
    transition: left .3s ease-in-out;
    background: #f5f6fa;
}
.content{
    width: auto;
    min-width: 1024px;
    margin: 15px 15px 20px;
}
</style>