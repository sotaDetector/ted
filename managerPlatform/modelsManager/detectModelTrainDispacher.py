from flask import Blueprint,request

from managerPlatform.bean.detectModelTrainVersion import detectModelTrainVersion
from managerPlatform.modelsManager.detectModelTrainService import detectModelTrainService

detect_model_train_blp = Blueprint("detectModelTrainDispacher", __name__, url_prefix="/detectModelTrain")

modelTrainService=detectModelTrainService()

@detect_model_train_blp.route('/detectModelVersionTrain', methods=['POST'])
def detectModelVersionTrain():

    jsonData=request.get_json()

    modelTrainVersionIns=detectModelTrainVersion.convertToBean(jsonData)

    return modelTrainService.detectModelVersionTrain(modelTrainVersionIns)