
from flask import Blueprint, request

from managerPlatform.imgClsModel.imgClsTrainService import imgClsTrainService

img_cls_train_blp = Blueprint("imgClsTrainDispacher", __name__, url_prefix="/imgClsModel")

imgClsTrain=imgClsTrainService()

@img_cls_train_blp.route("/imgClsModelTrain", methods=['POST'])
def imgClsModelTrain():
    jsonData = request.get_json()
    return imgClsTrain.imgClsModelTrain(jsonData)
