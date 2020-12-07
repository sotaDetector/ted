import json


class pageBean:

    def __init__(self,jsonData):
        self.page=jsonData["pageIndex"]
        self.pageSize=jsonData['pageSize']
        self.skipIndex=(self.page-1)*self.pageSize


    def set_totalCount(self,totalCount):
        self.totalCount=totalCount
        if (self.totalCount % self.pageSize)==0:
            self.totalPages=self.totalCount // self.pageSize
        else:
            self.totalPages = (self.totalCount // self.pageSize)+1


    def set_dataList(self,dataList):

        self.dataList=json.loads(dataList.to_json())

    def set_numpy_dataList(self, dataList):

        self.dataList = dataList


