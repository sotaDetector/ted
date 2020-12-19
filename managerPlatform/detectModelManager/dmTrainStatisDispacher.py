from flask import Blueprint, request

from managerPlatform.detectModelsManager.dmTrainStatisService import dmTrainStatisService

dm_train_statis_blp = Blueprint("dmTrainStatisDispacher", __name__, url_prefix="/dmTrainStatis")


dmTrainStatisSer=dmTrainStatisService()

"""
    获取训练数据统计
"""
@dm_train_statis_blp.route('/getTrainStatistics', methods=['POST'])
def getTrainStatistics():

    jsonData=request.get_json()


    return dmTrainStatisSer.getTrainStatistics(jsonData)