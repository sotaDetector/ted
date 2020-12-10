from flask import Blueprint, request

from managerPlatform.bean.user.userBean import userBean
from managerPlatform.userManager.userManagerService import userManagerService

user_manager_blp = Blueprint("userManagerDispacher", __name__, url_prefix="/user")


userService=userManagerService()
"""
    管理员用 添加用户
"""
@user_manager_blp.route('/userRegister', methods=['POST'])
def userRegister():

    jsonData = request.get_json()

    user=userBean.convertToBean(jsonData)

    return userService.userRegister(user)


@user_manager_blp.route('/userLogin', methods=['POST'])
def userLogin():

    jsonData = request.get_json()

    return userService.userLogin(jsonData)


@user_manager_blp.route('/loginOut', methods=['POST'])
def loginOut():

    return userService.loginOut()