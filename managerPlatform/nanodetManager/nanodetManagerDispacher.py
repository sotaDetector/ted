from flask import Blueprint, request

from managerPlatform.nanodetManager.nanodetManagerService import nanodetService

nanodet_manager_blp = Blueprint("nanodetDispacher", __name__, url_prefix="/nanodet")

nanodetSer=nanodetService()

@nanodet_manager_blp.route("/nanodeModelTrain", methods=['POST'])
def nanodeModelTrain():
    jsonData = request.get_json()
    return nanodetSer.nanodeModelTrain(jsonData)
