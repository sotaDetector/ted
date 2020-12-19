from flask import request, Blueprint, Response

from managerPlatform.streamPlayerService.mediaPlayerService import mediaPlayerService

media_Player_blp = Blueprint("mediaPlayerDispacher", __name__, url_prefix="/mediaPlayer")

mediaPlayerSer=mediaPlayerService()

@media_Player_blp.route("/videoPlayer")
def videoPlayer():
    sessionId=request.args.get("videoPlayId")
    return Response(mediaPlayerSer.genFramesFromVideo(sessionId), mimetype='multipart/x-mixed-replace; boundary=frame')


@media_Player_blp.route("/liveStreamPlayer")
def liveStreamPlayer():
    sessionId=request.args.get("videoPlayId")
    return Response(mediaPlayerSer.genFramesFromLiveStream(sessionId), mimetype='multipart/x-mixed-replace; boundary=frame')