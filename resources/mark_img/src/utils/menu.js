export const menuList = [{
  menuId: 1,
  menuName: '数据管理',
  url: '',
  children: [{
    menuId: 2,
    menuName: '数据集管理',
    url: 'dataManage'
  },{
    menuId: 3,
    menuName: '数据标注',
    url: 'markData'
  }]
},{
  menuId: 4,
  menuName: '模型管理',
  url: '',
  children: [{
    menuId: 5,
    menuName: '模型管理',
    url: 'modelManage'
  }]
},{
  menuId: 6,
  menuName: '模型调用',
  url: '',
  children: [{
    menuId: 7,
    menuName: '图片检测',
    url: 'imgDetect'
  },{
    menuId: 8,
    menuName: '视频检测',
    url: 'videoDetect'
  },{
    menuId: 9,
    menuName: '视频流检测',
    url: 'flowDetect'
  }]
}]