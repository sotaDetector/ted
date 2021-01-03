from flask import Blueprint, request, send_from_directory

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.detectModelManager.detectModelTrainService import detectModelTrainService

detect_model_train_blp = Blueprint("detectModelTrainDispacher", __name__, url_prefix="/detectModelTrain")

modelTrainService=detectModelTrainService()

@detect_model_train_blp.route('/DMVersionTrain', methods=['POST'])
def detectModelVersionTrain():

    jsonData=request.get_json()


    return modelTrainService.detectModelVersionTrain(jsonData)



@detect_model_train_blp.route('/getDMVersionList', methods=['POST'])
def getDMVersionList():

    jsonData=request.get_json()


    return modelTrainService.getDMVersionList(jsonData)


@detect_model_train_blp.route('/getDMVersionNameList', methods=['POST'])
def getDetectModelVersionList():

    jsonData=request.get_json()


    return modelTrainService.getDetectModelVersionNameList(jsonData)


@detect_model_train_blp.route('/getDMVersionDetail', methods=['POST'])
def getDMVersionDetail():

    jsonData=request.get_json()


    return modelTrainService.getDMVersionDetail(jsonData)


@detect_model_train_blp.route('/delDMVersion', methods=['POST'])
def delDMVersion():

    jsonData=request.get_json()


    return modelTrainService.delDMVersion(jsonData)


#下载检测模型
@detect_model_train_blp.route('/downloadDetectModel/<dmtvid>', methods=['POST','GET'])
def imageItem(dmtvid):

    filePath=modelTrainService.getDownloadModelUrl(dmtvid)
    basePath=filePath[:filePath.rindex("/")]
    filePath=filePath[filePath.rindex("/")+1:]

    return send_from_directory(basePath,filePath,as_attachment=True)

