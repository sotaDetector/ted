from flask import Blueprint, request, session, send_from_directory, make_response
from flask_cors import CORS,cross_origin
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.common.baseBean.pageBean import pageBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.config.configUtils import configUtils
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
    dsName=None
    if data.keys().__contains__("dsName"):

        dsName = data['dsName']
    pageItem = pageBean(data)
    return dsService.getDataSetPages(pageItem,dsName)


@dsm_blp.route('/getAllDSNamesList', methods=['POST'])
def getAllDSNamesList():

    return dsService.getAllDSNamesList()


@dsm_blp.route('/getDataSetDetail', methods=['POST'])
def getDataSetDetail():
    dsId = request.get_json()['dsId']
    return dsService.getDataSetDetail(dsId)


@dsm_blp.route('/updateDataSet', methods=['POST'])
def updateDataSet():
    data=request.get_json()
    return dsService.updateDataSet(data)


@dsm_blp.route('/delDataSet', methods=['POST'])
def delDataSet():
    dsId = request.get_json()['dsId']
    return dsService.delDataSet(dsId)


@dsm_blp.route('/upImageData', methods=['POST'])
def upImageData():
    print("up")
    # get parameters
    dsId = request.form.get("dsId")

    fileType = request.form.get("fileType")
    compreImgPack,imageslist=None,None
    if fileType==ConstantUtils.UP_FILE_TYPE_COMPRESSFILE:
        compreImgPack = request.files["compreImgPack"]
    elif fileType==ConstantUtils.UP_FILE_TYPE_IMAGEFILE:
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


@dsm_blp.route('/delImageItem', methods=['POST'])
def delImageItem():
    ditId = request.get_json()['ditId']
    return dsService.delImageItem(ditId)



@dsm_blp.route('/getImageItemDetail', methods=['POST'])
def getImageItemDetail():
    queryData = request.get_json()
    return dsService.getImageItemDetail(queryData)


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


@dsm_blp.route('/imageItem/<filePath>', methods=['POST','GET'])
def imageItem(filePath):
    return send_from_directory(ConstantUtils.dataBasePath,filePath.replace("_","/"),conditional=True)
