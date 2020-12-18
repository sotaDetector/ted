from flask import Blueprint, request

from managerPlatform.detectService.detectServiceCallerService import detectServiceCallerService

dts_caller_blp = Blueprint("dtsCallerDispacher", __name__, url_prefix="/dtsCaller")

detectServiceCaller=detectServiceCallerService()

@dts_caller_blp.route('/detectImage', methods=['POST'])
def getSingleImageDetectResult():

    dtsServiceKey=request.form.get("dtsServiceKey")
    dtsSecret = request.form.get("dtsSecret")
    imgData = request.files["detectedImage"]
    threshold = request.form.get('threshold')

    return detectServiceCaller.detectImage(dtsServiceKey,dtsSecret,threshold,imgData)