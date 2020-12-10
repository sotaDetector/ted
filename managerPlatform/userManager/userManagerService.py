from flask import session, redirect, url_for

from managerPlatform.bean.user.userBean import userBean
from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class userManagerService:

    def userRegister(self,user):

        user.save()
        return resultPackerUtils.save_success()


    def userLogin(self,data):
        userList=userBean.objects(userLoginAccount=data['userLoginAccount'],userLoginPass=data['userLoginPass'])

        if userList!=None and len(userList)>0:

            resultMap={
                "userName":userList[0]['userName']
            }
            session["userId"]=userList[0]['uid']
            return resultPackerUtils.packCusResult(resultMap)
        else:
            return resultPackerUtils.packErrorMsg(resultPackerUtils.EC_NAME_PASS_ERROR)

    def loginOut(self):
        session.pop("userId")
        return redirect(url_for('login'))






