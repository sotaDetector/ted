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
    dmName=data['dmName']
    pageItem=pageBean(data)

    return dctMoldeService.getDetectModelsPages(pageItem,dmName)

@detect_model_blp.route('/updateDetectModel', methods=['POST'])
def updateDetectModel():
    jsonData = request.get_json()
    return dctMoldeService.updateDetectModel(jsonData)