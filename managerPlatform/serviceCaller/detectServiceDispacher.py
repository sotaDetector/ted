from flask import Blueprint, request

from managerPlatform.serviceCaller.detectServiceImpl import detectServiceImpl

detect_service_blp = Blueprint("detectServiceDispacher", __name__, url_prefix="/detectService")


detectSerice=detectServiceImpl()

@detect_service_blp.route('/launchDetectService', methods=['POST'])
def launchDetectService():

    jsonData = request.get_json()



    return detectSerice.launchDetectService(jsonData)