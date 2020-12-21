<template>
  <div class="login">
    <div class="inner">
      <!-- <img src="../assets/images/avatar.jpg" alt="" class="avatar"> -->
      <Form class="formItem ivu-form-label-left" ref="userInfo" :model="userInfo" :rules="rules">
        <FormItem prop="user">
          <Input type="text" v-model="userInfo.user" placeholder="用户名">
          </Input>
        </FormItem>
        <FormItem prop="password" style="margin-bottom:10px;">
          <Input type="password" v-model="userInfo.password" placeholder="密码">
          </Input>
        </FormItem>
        <div class="ivu-form-item">
          <label class="ivu-form-item-label">
            <Checkbox v-model="checked">记住密码</Checkbox>
          </label>
          <div class="register" @click="register">
            注册账号
          </div>
        </div>
        <FormItem>
          <Button style="height:45px;" long type="primary" @click="handleSubmit('userInfo')">登 录</Button>
        </FormItem>
      </Form>
    </div>
  </div>
</template>

<script>
import { loginMethod } from '@/network/login'
import { menuList } from '@/utils/menu'
let Base64 = require('js-base64').Base64
export default {
  name: 'Login',
  data () {
    return {
      menuList,
      checked: true,
      userInfo: {
        name: '',
        password: ''
      },
      rules: {
        name: [{ required: true, message: '请输入用户名' }],
        password: [
          { required: true, message: '请输入密码' },
          { min: 6, message: '最少 6 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.getCookie()
  },
  methods: {
    register () {
      this.$router.push({ path: '/register' })
    },
    //登录方法
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          // 引用login.js中的方法，.then回调
          this.$Spin.show()
          loginMethod(this.userInfo.user, this.$md5(this.userInfo.password)).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              const self = this;
              if(self.checked == true) {
                // console.log("checked == true");
                //传入账号名，密码，和保存天数3个参数
                self.setCookie(self.userInfo.user, Base64.encode(this.userInfo.password), 7);
              } else {
                // console.log("清空Cookie");
                //清空Cookie
                self.clearCookie();
              }
              this.$Message.success('登录成功!');
              // 将用户token,menuList,userName保存到vuex中
              //type用户类型：1-运营；2-渠道；3-企业
              this.menuList.some(item => {
                if(item.children && item.children.length > 0) {
                  this.$router.push('/' + item.children[0].url)
                  return true
                }
              })
            } else {
              if(data.data && data.data.errorMsg) {
                this.$Message.error(data.data.errorMsg);
              } else {
                this.$Message.error(data.errorMsg);
              }
            }
          })
        } else {
          this.$Message.error('登录失败!');
        }
      })
    },
    //设置cookie
    setCookie (c_name, c_pwd, exdays) {
      var exdate = new Date(); //获取时间
      exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); //保存的天数
      //字符串拼接cookie
      window.document.cookie =
        "userName" + "=" + c_name + ";path=/;expires=" + exdate.toGMTString();
      window.document.cookie =
        "userPwd" + "=" + c_pwd + ";path=/;expires=" + exdate.toGMTString();
    },
    //获取cookie
    getCookie () {
      if(document.cookie.length > 0) {
        var arr = document.cookie.split("; "); //这里显示的格式需要切割一下自己可输出看下
        for(var i = 0; i < arr.length; i++) {
          var arr2 = arr[i].split("="); //再次切割
          //判断查找相对应的值
          if(arr2[0] == "userName") {
            this.userInfo.user = arr2[1]; //保存到保存数据的地方
          } else if(arr2[0] == "userPwd") {
            this.userInfo.password = Base64.decode(arr2[1]);
          }
        }
      }
    },
    //清除cookie
    clearCookie: function () {
      this.setCookie("", "", -1); //修改2值都为空，天数为负1天就好了
    }
  }
}
</script>

<style lang="scss" scoped>
.login {
  width: 100%;
  height: 100vh;
  background: url("../assets/img/login.jpg") no-repeat center;
  background-size: 100% 100%;
  overflow: hidden;
  position: relative;
}
.inner {
  width: 330px;
  height: 280px;
  background: #fff;
  border-radius: 6px;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -165px;
  margin-top: -140px;
  padding: 50px 20px 20px;
}
.register {
  float: right;
  width: auto;
  margin-top: 10px;
  font-size: 12px;
  text-decoration: underline;
  cursor: pointer;
}
</style>
