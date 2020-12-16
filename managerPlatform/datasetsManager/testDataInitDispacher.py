from flask import Blueprint, request

from managerPlatform.datasetsManager.testDataInitService import testDataInitService

test_data_init_blp = Blueprint("testDataInitDispacher", __name__, url_prefix="/testDataInit")

testDataInit=testDataInitService()

@test_data_init_blp.route('/initTrainModelDataSet', methods=['POST'])
def initTrainModelDataSet():

    queryData = request.get_json()

    return testDataInit.initTrainModelDataSet(queryData)
