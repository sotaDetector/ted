from flask import Blueprint,request

from managerPlatform.modelsManager.detectModelTrainService import detectModelTrainService

detect_model_train_blp = Blueprint("detectModelTrainDispacher", __name__, url_prefix="/detectModelTrain")

modelTrainService=detectModelTrainService()

@detect_model_train_blp.route('/detectModelVersionTrain', methods=['POST'])
def detectModelVersionTrain():

    jsonData=request.get_json()


    return modelTrainService.detectModelVersionTrain(jsonData)



"""
    获取训练数据统计
"""
@detect_model_train_blp.route('/getTrainStatistics', methods=['POST'])
def getTrainStatistics():

    jsonData=request.get_json()


    return modelTrainService.detectModelVersionTrain(jsonData)