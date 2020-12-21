from flask import Blueprint, request

from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.detectModelValidation.imageDetectService import imageDetectService

iamge_detect_blp = Blueprint("imageDetectDispacher", __name__, url_prefix="/imageDetect")

imgDetefctService=imageDetectService()

@iamge_detect_blp.route('/getSingleImageDetectResult', methods=['POST'])
def getSingleImageDetectResult():
    serviceSessionId=request.form.get(ConstantUtils.serviceSessionId)
    imgData = request.files["detectedImage"]
    threshold = request.form.get('threshold')

    return imgDetefctService.getSingleImageDetectResult(serviceSessionId,threshold,imgData)