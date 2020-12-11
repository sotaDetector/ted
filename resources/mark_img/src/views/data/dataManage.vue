<template>
  <div>
    <div class="container_title">
      <!-- 面包屑 -->
      <!-- <Breadcrumb>
        <BreadcrumbItem>企业管理</BreadcrumbItem>
      </Breadcrumb> -->
      <!-- 操作按钮 -->
      <div class="ops_btn">
        <Button type="primary" ghost size='small' @click="addModal">新增</Button>
      </div>
    </div>
    <div class="container_info">
      <div class="container_box">
        <!-- 查询条件 -->
        <div class="query_option">
          <Input style="width: 200px;" v-model="search.dsName" placeholder="请输入数据集名称"></Input>
          <span class="query_btn">
            <Button type="info" @click="queryPageInfo">查询</Button>
            <Button @click="clearSearch">重置</Button>
          </span>
        </div>
        <!-- 表格列表 -->
        <div class="container_table">
          <Table :columns="columns" :data="pageInfo.data"></Table>
        </div>
        <div class="pageInfo">
          <Page size="small" :total="total" :page-size='pagesize' @on-change="handleChange" show-total show-elevator></Page>
        </div>
      </div>
    </div>
    <!-- 模态框 -->
    <Modal class="sys_modal" v-model="modal_delete" class-name="vertical_modal" width="316">
      <div class="modal_body modal_body_delete">
        <p>
          <img src="@/assets/img/warn_tip.png" alt="">
          您确定要删除该企业吗?
        </p>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="deleteMethod(channelId)">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel()">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_add" width="450" title="新增企业">
      <div class="modal_body">
        <Form ref="addInfo" label-position="left" :model="addInfo" :rules="ruleValidate" :label-width="110">
          <FormItem label="数据集名称" prop="dsName">
            <Input v-model="addInfo.dsName"></Input>
          </FormItem>
          <FormItem label="数据集类型" prop="dsType">
            <Select v-model="addInfo.dsType">
              <Option :value=1>图片</Option>
              <!-- <Option :value=1>开启</Option> -->
            </Select>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="addInfoMethod('addInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('addInfo')">取消</Button>
      </div>
    </Modal>
    <Modal class="sys_modal" v-model="modal_modify" width="450" title="修改企业">
      <div class="modal_body">
        <Form ref="modifyInfo" label-position="left" :model="modifyInfo" :rules="ruleValidate" :label-width="110">
          <FormItem label="数据集名称" prop="dsName">
            <Input v-model="modifyInfo.dsName"></Input>
          </FormItem>
          <FormItem label="数据集类型" prop="dsType">
            <Select v-model="modifyInfo.dsType">
              <Option :value=1>图片</Option>
              <!-- <Option :value=1>开启</Option> -->
            </Select>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="primary" class="confirm_btn" ghost @click="modifyInfoMethod('modifyInfo')">确定</Button>
        <Button type="default" class="clear_btn" @click="cancel('modifyInfo')">取消</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  mounted () {
    this.queryPageInfo()
  },
  data () {
    return {
      total: 0,// 初始化信息总条数
      pageNow: 1,
      pagesize: 20,// 每页显示多少条
      search: {},
      modal_delete: false,
      modal_add: false,
      modal_modify: false,
      addInfo: {
        dsName: '',
        dsType: 1,
      },
      ruleValidate: {
        dsName: [
          { required: true, message: '请输入企业名称', trigger: 'blur' },
        ],
        dsType: [
          { required: true, message: '请输入登录用户名', trigger: 'blur', type: 'number' }
        ],
      },

      modifyInfo: {
        dsName: '',
        dsType: ''
      },
      columns: [
        {
          "title": "数据集名称",
          "align": "center",
          "key": "dsName"
        }, {
          "title": "标注类型",
          "align": "center",
          "key": "dsType"
        }, {
          "title": "标注进度",
          "align": "center",
          "key": "phoneNum"
        }, {
          "title": "标签数量",
          "align": "center",
          "key": "email",
          "width": 190,
        }, {
          "title": "标签",
          "align": "center",
          "key": "email",
          "width": 190,
        }, {
          'title': '操作',
          'align': 'center',
          'key': 'action',
          render: (h, params) => {
            return h('div', [
              h('span', {
                class: 'iconfont icon-bianji',
                style: {
                  fontSize: '18px', // 改变icon的样式
                  cursor: 'pointer'
                },
                on: {
                  click: () => {
                    // 点击操作事件
                    this.modifyModal(params.row.enterpriseId)
                  }
                }
              })
            ])
          }
        }],
      pageInfo: {},
    }
  },
  methods: {
    // 获取分页信息
    queryPageInfo () {
      let params = {
        pageIndex: this.pageNow,
        pageSize: this.pagesize,
        dsName: this.search.dsName
      }
      this.$Spin.show()
      this.$post('/dsc/getDataSetPages', params).then(data => {
        this.$Spin.hide()
        if(data.rs === 1) {
          this.pageInfo = data.pageInfo;
          this.total = data.pageInfo.totalRows;//总数
          this.chosePage = data.pageInfo.page;//选择页
          this.pageNow = data.pageInfo.page;//当前页
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    //分页
    handleChange (page) {
      this.pageNow = page;//赋值当前页
      this.queryPageInfo();
    },
    // 删除弹框
    deleteModal (channelId) {
      this.channelId = channelId
      this.modal_delete = true
    },
    // 确认删除
    deleteMethod (channelId) {
      this.$Spin.show()
      this.$post('/channel/deleteChannel', {
        channelId: channelId
      }).then(data => {
        if(data.rs === 1) {
          this.$Spin.hide()
          this.modal_delete = false
          this.$Message.success('删除成功!');
          this.queryPageInfo();
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    // 新增弹框
    addModal () {
      this.modal_add = true
      this.addInfo.id = this.defaultRoleId
    },
    // 确认新增
    addInfoMethod (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          this.$Spin.show()
          this.$post('/dsc/addDataSet', {
            dsName: this.addInfo.dsName,
            dsType: this.addInfo.dsType,
          }).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.modal_add = false
              this.$Message.success('新增成功!');
              this.$refs[name].resetFields();// 清空
              this.queryPageInfo();
            } else {
              if(data.data && data.data.errorMsg) {
                this.$Message.error(data.data.errorMsg);
              } else {
                this.$Message.error(data.errorMsg);
              }
            }
          })
        } else {
          this.$Message.error('新增失败!');
        }
      })
    },
    // 编辑弹框
    modifyModal (enterpriseId) {
      this.modal_modify = true
      this.$post('/enterprise/queryDetails', {
        enterpriseId: enterpriseId
      }).then(data => {
        if(data.rs === 1) {
          this.modifyInfo = data.enterpriseInfo
          this.modifyInfo.serviceBeginDate = new Date(data.enterpriseInfo.serviceBeginDate)
          this.modifyInfo.serviceEndDate = new Date(data.enterpriseInfo.serviceEndDate)
        } else {
          if(data.data && data.data.errorMsg) {
            this.$Message.error(data.data.errorMsg);
          } else {
            this.$Message.error(data.errorMsg);
          }
        }
      })
    },
    // 确认编辑
    modifyInfoMethod (name) {
      this.$refs[name].validate((valid) => {
        if(valid) {
          this.$Spin.show()
          this.$post('/enterprise/updateEnterpriseInfo.json', {
            dsName: this.modifyInfo.dsName,
            dsType: this.modifyInfo.dsType,
          }).then(data => {
            this.$Spin.hide()
            if(data.rs === 1) {
              this.modal_modify = false
              this.$Message.success('修改成功!');
              this.queryPageInfo();
            } else {
              if(data.data && data.data.errorMsg) {
                this.$Message.error(data.data.errorMsg);
              } else {
                this.$Message.error(data.errorMsg);
              }
            }
          })
        } else {
          this.$Message.error('修改失败!');
        }
      })
    },
    cancel (name) {
      this.modal_add = false
      this.modal_modify = false
      this.modal_delete = false
      if(name) {
        this.$refs[name].resetFields();
      }
    },
    // 重置
    clearSearch () {
      this.search = {
        dsName: ''
      }
    }
  }
}
</script>


<style lang="scss" scoped>
</style>