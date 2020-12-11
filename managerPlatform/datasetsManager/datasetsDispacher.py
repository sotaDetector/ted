from flask import Blueprint, request, session
from flask_cors import CORS,cross_origin
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.common.baseBean.pageBean import pageBean
from managerPlatform.datasetsManager.datasetsService import datasetsService

dsm_blp = Blueprint("datasetsDispacher", __name__, url_prefix="/dsc")



dsService = datasetsService()


@dsm_blp.route('/addDataSet', methods=['POST'])
def addDataSet():

    datasetsItem=datasetsBean.convertToBean(request.get_json(),session)

    return dsService.addDataSet(datasetsItem)


@dsm_blp.route('/getDataSetPages', methods=['POST'])
def getDataSetPages():
    data = request.get_json()
    print("userId")
    print(session.get("userId"))
    dsName = data['dsName']
    pageItem = pageBean(data)
    return dsService.getDataSetPages(pageItem,dsName)


@dsm_blp.route('/upImageData', methods=['POST'])
def upImageData():
    # get parameters
    dsId = request.form.get("dsId")

    fileType = request.form.get("fileType")

    compreImgPack = request.files["compreImgPack"]

    imageslist = request.files.getlist("imageslist")

    # 获取该文件下所有的图片
    return dsService.upImageData(dsId, fileType, compreImgPack, imageslist)

"""
获取某个数据集下所有的图片
"""
@dsm_blp.route('/getImageItemList', methods=['POST'])
def getImageItemList():
    data = request.get_json()
    pageItem = pageBean(data)
    return dsService.getImageItemList(pageItem,data)


"""
上传图片标注数据
"""
@dsm_blp.route('/upImageItemRecLabels', methods=['POST'])
def upImageItemRecLabels():
    data = request.get_json()

    return dsService.upImageItemRecLabels(data)



"""
上传图片标注数据
"""
@dsm_blp.route('/initTestData', methods=['POST'])
def initTestData():

    return dsService.initTestData()
