from flask import Blueprint, request

from managerPlatform.bean.detectModel.detectModelBean import detectModelBean
from managerPlatform.common.baseBean.pageBean import pageBean
from managerPlatform.modelsManager.detectModelService import detectModelService

detect_model_blp = Blueprint("detectModelDispacher", __name__, url_prefix="/detectModel")

dctMoldeService = detectModelService()


@detect_model_blp.route('/addDetectModel', methods=['POST'])
def addDetectModel():

    jsonData=request.get_json()

    dataLabelIns=detectModelBean.convertToBean(jsonData)

    return dctMoldeService.addDetectModel(dataLabelIns)


@detect_model_blp.route('/getDetectModelsPages', methods=['POST'])
def getDetectModelsPages():
    data = request.get_json()
    if data.keys().__contains__('dmName'):
        dmName=data['dmName']
    else:
        dmName=None
    pageItem=pageBean(data)

    return dctMoldeService.getDetectModelsPages(pageItem,dmName)

@detect_model_blp.route('/updateDetectModel', methods=['POST'])
def updateDetectModel():
    jsonData = request.get_json()
    return dctMoldeService.updateDetectModel(jsonData)


@detect_model_blp.route('/getDetectModelDetail', methods=['POST'])
def getDetectModelDetail():
    dmId=request.get_json()['dmId']
    return dctMoldeService.getDetectModelDetail(dmId)


@detect_model_blp.route('/delDetectModel', methods=['POST'])
def delDetectModelDetail():
    dmId=request.get_json()['dmId']
    return dctMoldeService.delDetectModelDetail(dmId)