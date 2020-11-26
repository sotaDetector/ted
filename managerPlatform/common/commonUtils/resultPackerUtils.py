import json
from bson import json_util
from flask import make_response


class resultPackerUtils:
    _resultTag = "rs"
    _resultDataTag="data"
    _success_tag = 1

    @classmethod
    def save_success(cls):
        result = {
            cls._resultTag: cls._success_tag
        }
        return json.dumps(result)

    @classmethod
    def update_success(cls):
        result = {
            cls._resultTag: cls._success_tag
        }
        return json.dumps(result)

    @classmethod
    def packDataListResults(cls,dataList):
        result = {
            cls._resultTag: cls._success_tag,
            cls._resultDataTag:json.loads(dataList)
        }
        return result

    @classmethod
    def packPageResult(cls,data):
        result = {
            cls._resultTag: cls._success_tag,
            "pageData":data.__dict__
        }
        return json.dumps(result)
