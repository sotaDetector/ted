from flask import Blueprint, request

from managerPlatform.bean.dataLabelBean import dataLabelBean
from managerPlatform.dataLabel.dataLabelService import dataLabelService

dataLabel_blp = Blueprint("datalLabelDispacher", __name__, url_prefix="/dataLabel")
dlabelService = dataLabelService()


"""
     2.1 添加数据标签
"""
@dataLabel_blp.route('/addDataLabel', methods=['POST'])
def addDataLabel():
    data = request.get_json()
    dataLabelIns=dataLabelBean.convertToBean(data)

    return dlabelService.addDataLabel(dataLabelIns)


"""
     2.2 修改数据标签
"""
@dataLabel_blp.route('/updateDataLabel', methods=['POST'])
def updateDataLabel():
    data = request.get_json()

    return dlabelService.updateDataLabel(data)

"""
    2.4 根据数据集id获取所有标签
"""
@dataLabel_blp.route('/getAllDataLabelByDsid', methods=['POST'])
def getAllDataLabelByDsid():
    data = request.get_json()
    return dlabelService.getAllDataLabelByDsid(data)


@dataLabel_blp.route('/delDataLabel', methods=['POST'])
def delDataLabel():
    jsonData=request.get_json()
    dlid=jsonData['dlid']
    return dlabelService.delDataLabel(dlid)
