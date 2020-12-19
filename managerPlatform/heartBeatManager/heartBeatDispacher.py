from flask import Blueprint, request

from managerPlatform.heartBeatManager.heartBeatService import heartBeatService

heart_beat_blp = Blueprint("heartBeatDispacher", __name__, url_prefix="/heartBeat")

heartBeantSer=heartBeatService()

@heart_beat_blp.route("/sendDetectHeartbeat", methods=['POST'])
def sendDetectHeartbeat():
    jsonData = request.get_json()
    return heartBeantSer.sendDetectHeartbeat(jsonData)
