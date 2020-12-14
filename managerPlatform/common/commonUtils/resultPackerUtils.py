import json
from bson import json_util
from flask import make_response


class resultPackerUtils:
    EC_NAME_PASS_ERROR = 1001

    EC_NO_EVALUATE_SESSION=3001
    ERRORMAP = {
        EC_NAME_PASS_ERROR: "用户名或密码错误",
        EC_NO_EVALUATE_SESSION:"未启动校验服务或服务已过期！"
    }

    _resultTag = "rs"
    _resultDataTag="data"
    _errorCodeTag="erroCode"
    _success_tag = 1

    @classmethod
    def save_success(cls):
        result = {
            cls._resultTag: cls._success_tag,
            cls._resultDataTag:"添加成功！"
        }
        return json.dumps(result)

    @classmethod
    def update_success(cls):
        result = {
            cls._resultTag: cls._success_tag,
            cls._resultDataTag: "修改成功！"
        }
        return json.dumps(result)

    @classmethod
    def packDataListResults(cls,dataList=None,idName=None):

        if idName:
            dataList=dataList.replace("_id", idName)

        result = {
            cls._resultTag: cls._success_tag,
            cls._resultDataTag: json.loads(dataList)
        }
        return result

    @classmethod
    def packDataItemResults(cls,dataItem,idName=None):
        if idName:
            dataItem=dataItem.replace("_id",idName)
        result = {
            cls._resultTag: cls._success_tag,
            cls._resultDataTag: json.loads(dataItem)[0]
        }
        return result

    @classmethod
    def packJsonListResults(cls, dataList):
        result = {
            cls._resultTag: cls._success_tag,
            cls._resultDataTag: dataList
        }
        return result


    @classmethod
    def packPageResult(cls,data):
        result = {
            cls._resultTag: cls._success_tag,
            "pageData":data.__dict__
        }
        return json.dumps(result)

    @classmethod
    def packErrorMsg(cls,errorCode):
        result = {
            cls._resultTag: cls._success_tag,
            cls._errorCodeTag: errorCode,
            cls._resultDataTag:cls.ERRORMAP[errorCode]
        }
        return json.dumps(result)

    @classmethod
    def packCusResult(cls,resultMap):
        resultMap[cls._resultTag]=cls._success_tag
        return json.dumps(resultMap)




