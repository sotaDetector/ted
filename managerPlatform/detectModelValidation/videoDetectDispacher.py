from flask import Blueprint, request, Response

from managerPlatform.detectModelValidation.videoDetectService import videoDetectService

video_detect_blp = Blueprint("vedioDetectDispacher", __name__, url_prefix="/videoDetect")

videoDetectSer=videoDetectService()

@video_detect_blp.route('/getVideoDetectResult', methods=['POST'])
def getVideoDetectResult():
    serviceSessionId=request.form.get("serviceSessionId")
    detectVideo = request.files["detectVideo"]
    threshold = request.form.get('threshold')

    return videoDetectSer.getVideoDetectResult(serviceSessionId,threshold,detectVideo)



