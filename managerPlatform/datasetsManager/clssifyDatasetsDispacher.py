from flask import Blueprint, request

from managerPlatform.common.baseBean.pageBean import pageBean
from managerPlatform.datasetsManager.clssifyDatasetsService import clssifyDatasetsService

clsImgDS_blp = Blueprint("classifyImgDSDispacher", __name__, url_prefix="/clsImgDS")

classifyService=clssifyDatasetsService()

"""
上传图像分类标注数据
"""
@clsImgDS_blp.route('/upClsImgItem', methods=['POST'])
def upClassifyImageItem():
    data = request.get_json()

    return classifyService.upClassifyImageItem(data)



"""
获取某个数据集下所有的图片
"""
@clsImgDS_blp.route('/getClsImgItemList', methods=['POST'])
def getClsImgItemList():
    data = request.get_json()
    pageItem = pageBean(data)
    return classifyService.getClsImgItemList(pageItem,data)


"""
获取某个数据集下所有的图片
"""
@clsImgDS_blp.route('/getClsImgDetail', methods=['POST'])
def getClsImgDetail():
    data = request.get_json()
    return classifyService.getClsImgDetail(data)



"""
获取某个数据集下所有的图片
"""
@clsImgDS_blp.route('/delClsImgItem', methods=['POST'])
def delClsImgItem():
    data = request.get_json()
    return classifyService.delClsImgItem(data)