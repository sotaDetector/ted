<template>
  <div class="login">
    <div class="inner">
      <!-- <img src="../assets/images/avatar.jpg" alt="" class="avatar"> -->
      <div class="title">TED千眼通用目标检测平台</div>
      <Form class="formItem ivu-form-label-left" ref="userInfo" :model="userInfo" :rules="rules">
        <FormItem prop="nick">
          <Input type="text" v-model="userInfo.nick" placeholder="昵称">
          </Input>
        </FormItem>
        <FormItem prop="user">
          <Input type="text" v-model="userInfo.user" placeholder="用户名">
          </Input>
        </FormItem>
        <FormItem prop="password" style="margin-bottom:10px;">
          <Input type="password" v-model="userInfo.password" placeholder="密码">
          </Input>
        </FormItem>
        <div class="ivu-form-item">
          <div class="go_login" @click="goLogin">
            已有账号，直接登录
          </div>
        </div>
        <FormItem>
          <Button style="height:40px;" long type="primary" @click="handleSubmit('userInfo')">注 册</Button>
        </FormItem>
      </Form>
    </div>
  </div>
</template>

<script>
import { registerMethod } from '@/network/login'
let Base64 = require('js-base64').Base64
export default {
  name: 'Register',
  data () {
    return {
      userInfo: {
        nick: '',
        user: '',
        password: ''
      },
      rules: {
        nick: [{ required: true, message: '请输入昵称' }],
        user: [{ required: true, message: '请输入用户名' }],
        password: [
          { required: true, message: '请输入密码' },
          { min: 6, message: '最少 6 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    goLogin () {
      this.$router.push('/login')
    },
    //登录方法
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          // 引用login.js中的方法，.then回调
          this.$Spin.show()
          registerMethod(this.userInfo.nick, this.userInfo.user, this.$md5(this.userInfo.password)).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.$Message.success('注册成功!');
              this.$router.push('/login')
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
}
.inner {
  width: 350px;
  height: 355px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -175px;
  margin-top: -177.5px;
  padding: 0 20px 20px;
}
.inner .title {
  text-align: center;
  line-height: 80px;
  font-size: 20px;
  background-image: linear-gradient(135deg, red, blue);
  -webkit-background-clip: text;
  color: transparent;
}
.go_login {
  float: right;
  width: auto;
  margin-top: 10px;
  font-size: 12px;
  text-decoration: underline;
  cursor: pointer;
}
</style>
