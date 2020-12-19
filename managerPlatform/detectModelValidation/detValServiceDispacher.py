from flask import Blueprint, request

from managerPlatform.serviceCaller.detValServiceImpl import detValServiceImpl

detect_service_blp = Blueprint("detectService", __name__, url_prefix="/detectService")


detValSerice=detValServiceImpl()

@detect_service_blp.route('/launchDetectService', methods=['POST'])
def launchDetectService():

    jsonData = request.get_json()



    return detValSerice.launchDetectService(jsonData)