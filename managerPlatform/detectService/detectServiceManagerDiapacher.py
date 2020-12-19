from flask import Blueprint, request, session

from managerPlatform.bean.detectService.detectServiceBean import detectServiceBean
from managerPlatform.common.baseBean.pageBean import pageBean
from managerPlatform.detectService.detectServiceManagerImpl import detectServiceImpl

dts_blp = Blueprint("detectServiceDispacher", __name__, url_prefix="/dts")


dsService=detectServiceImpl()
"""
     添加服务
"""
@dts_blp.route('/addDetectService', methods=['POST'])
def addDetectService():
    jsonData = request.get_json()

    return dsService.addDetectService(jsonData)


@dts_blp.route('/updateDetectService', methods=['POST'])
def updateDetectService():
    jsonData = request.get_json()

    return dsService.updateDetectService(jsonData)

@dts_blp.route('/delDetectService', methods=['POST'])
def delDetectService():
    jsonData = request.get_json()

    return dsService.delDetectService(jsonData)


@dts_blp.route('/getDetectServiceDetail', methods=['POST'])
def getDetectServiceDetail():
    jsonData = request.get_json()

    return dsService.getDetectServiceDetail(jsonData)


#更改服务状态
@dts_blp.route('/changeDtsSwitch', methods=['POST'])
def changeDtsSwitch():
    jsonData = request.get_json()

    return dsService.changeDtsSwitch(jsonData)




@dts_blp.route('/getDetectServicePageList', methods=['POST'])
def getDetectServicePageList():
    data = request.get_json()

    pageItem = pageBean(data)


    return dsService.getDetectServicePageList(pageItem)







