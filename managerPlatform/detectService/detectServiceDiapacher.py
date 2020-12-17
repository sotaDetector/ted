from flask import Blueprint, request, session

from managerPlatform.bean.detectService.detectServiceBean import detectServiceBean
from managerPlatform.common.baseBean.pageBean import pageBean
from managerPlatform.detectService.detectServiceImpl import detectServiceImpl

dts_blp = Blueprint("detectServiceDispacher", __name__, url_prefix="/dts")


dsService=detectServiceImpl()
"""
     添加服务
"""
@dts_blp.route('/addDetectService', methods=['POST'])
def addDetectService():
    jsonData = request.get_json()

    return dsService.addDetectService(jsonData)


@dts_blp.route('/getDetectServicePageList', methods=['POST'])
def getDetectServicePageList():
    data = request.get_json()

    pageItem = pageBean(data)


    return dsService.getDetectServicePageList(pageItem)







