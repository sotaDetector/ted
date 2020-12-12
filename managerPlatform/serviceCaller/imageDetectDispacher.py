from flask import Blueprint, request

from managerPlatform.serviceCaller.imageDetectService import imageDetectService

iamge_detect_blp = Blueprint("imageCameraDispacher", __name__, url_prefix="/imageDetect")

imgDetefctService=imageDetectService()

@iamge_detect_blp.route('/getSingleImageDetectResult', methods=['POST'])
def getSingleImageDetectResult():

    imgData = request.files["detectedImage"]
    dmId=request.form.get('dmId')
    threshold = request.form.get('threshold')

    return imgDetefctService.getSingleImageDetectResult(dmId,threshold,imgData)