import json
import os
import uuid
import numpy as np
from flask import session

from managerPlatform.bean.detectModel.detectModelVersion import detectModelTrainVersion
from managerPlatform.bean.trainDataset.classifyImageItem import classifyImageItem
from managerPlatform.bean.trainDataset.dataImageItem import dataImageItem
from managerPlatform.bean.trainDataset.dataLabelBean import dataLabelBean
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.bean.trainDataset.rectangleLabelBean import rectangleLabelBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.imageUtils import imageUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.dataLabel.dataLabelService import dataLabelService
from managerPlatform.datasetsManager.clssifyDatasetsService import clssifyDatasetsService

labelService = dataLabelService()


class datasetsService:

    def addDataSet(self, dsName):

        dsName.save()

        return resultPackerUtils.save_success()

    def getAllDSNamesList(self,jsonData):
        datasetsList = datasetsBean.objects(state=1,
                                            userId=session['userId'],
                                            cvTaskType=jsonData['cvTaskType']).only("dsId","dsName")

        return resultPackerUtils.packDataListResults(datasetsList.to_json(),"dsId")

    def getDataSetPages(self, pageItem, dsName):

        userSearchDict = {}
        if dsName != None:
            userSearchDict['dsName'] = {'$regex': dsName}

        totalCount = datasetsBean.objects(__raw__=userSearchDict,state=1,userId=session['userId']).count()


        #获取数据集

        datasetList = datasetsBean.objects(__raw__=userSearchDict,state=1,userId=session['userId']).order_by('-create_date').skip(
            pageItem.skipIndex).exclude("state","userId").limit(pageItem.pageSize)
        # only("dsName","dsType")

        #获取数据集下的所有标签
        dsIdList=[]
        for item in datasetList:
            dsIdList.append(item['dsId'])

        labelList=dataLabelBean.objects(dsId__in=dsIdList)

        labelMap={}
        for labelItem in labelList:
            dsId=labelItem['dsId']
            if labelMap.keys().__contains__(dsId):
                labelMap[dsId].append(labelItem['dlName'])
            else:
                labelMap[dsId]=[labelItem['dlName']]

        datasetsList=[]
        for item in datasetList:
            if labelMap.keys().__contains__(item['dsId']):
                labelList=labelMap[item['dsId']]
            else:
                labelList=[]
            datasetItem={
                "dsId":item['dsId'],
                "dsName":item['dsName'],
                "dsType":item['dsType'],
                "dsImageCount":item['dsImageCount'],
                "dsImgTagSP":item['dsImgTagSP'],
                "labelCount":len(labelList),
                "labelList":labelList,
                "cvTaskType":item['cvTaskType'],
                "cvTaskName":ConstantUtils.getCVTaskTypaName(item['cvTaskType'])
            }
            datasetsList.append(datasetItem)

        pageItem.set_totalCount(totalCount)

        pageItem.set_numpy_dataList(datasetsList)

        return resultPackerUtils.packPageResult(pageItem);


    def getDataSetDetail(self,dsId):
        result = datasetsBean.objects(dsId=dsId, state=1).exclude("state", "userId").to_json()
        return resultPackerUtils.packDataItemResults(result)


    def updateDataSet(self,data):
        datasetIns = datasetsBean.objects(dsId=data['dsId'])

        print(data['updateClolumn'])
        datasetIns.update(**data['updateClolumn'])

        return resultPackerUtils.update_success()

    def delDataSet(self,dsId):
        detectsetItem = datasetsBean.objects(dsId=dsId)
        detectsetItem.update(state=ConstantUtils.DATA_STATUS_DELETED)
        return resultPackerUtils.update_success()

    def upImageData(self, dsId, fileType, compreImgPack, imageslist):

        #获取dataset detail
        datasetItem = datasetsBean.objects(dsId=dsId, state=ConstantUtils.DATA_STATUS_ACTIVE).first()


        imageFiles = None

        folderName = str(uuid.uuid4())

        desFolderBasePath = ConstantUtils.dataBasePath + folderName

        imageNameList,imagePathList=None,None
        if fileType == ConstantUtils.UP_FILE_TYPE_COMPRESSFILE:
            imageNameList, imagePathList = self.saveCompressedFile(desFolderBasePath, compreImgPack)
        elif fileType == ConstantUtils.UP_FILE_TYPE_IMAGEFILE:
            imageNameList, imagePathList = self.saveMultiImages(desFolderBasePath, imageslist)

        # 保存到数据库
        #如果是图像分类数据集
        if datasetItem["cvTaskType"]==ConstantUtils.CV_TASK_TYPE_CLASSIFY:
            return self.dealClassifyDatasets(dsId,desFolderBasePath,folderName,imageNameList, imagePathList)

        saveImageItemList = []
        for i in range(imageNameList.__len__()):
            fileName = imageNameList[i]
            filePath = imagePathList[i]
            # 获取图片信息
            imageSize = imageUtils.getImageSize(desFolderBasePath + "/" + filePath)
            saveImageItemList.append(dataImageItem(
                ditFileName=fileName,
                ditFilePath=folderName + "/" + filePath,
                dsId=dsId,
                ditWidth=imageSize[0],
                ditHeight=imageSize[1],
                isLabeled=ConstantUtils.IMAGE_UNLABEL
            ))

        dataImageItem.objects.insert(saveImageItemList, load_bulk=False)
        #更新数据集数量
        self.updateDataSetStatisData(dsId)
        return resultPackerUtils.save_success()

    def dealClassifyDatasets(self,dsId,desFolderBasePath,folderName,imageNameList,imagePathList,):
        saveImageItemList = []
        for i in range(imageNameList.__len__()):
            fileName = imageNameList[i]
            filePath = imagePathList[i]
            # 获取图片信息
            imageSize = imageUtils.getImageSize(desFolderBasePath + "/" + filePath)
            saveImageItemList.append(classifyImageItem(
                ditFileName=fileName,
                ditFilePath=folderName + "/" + filePath,
                dsId=dsId,
                ditWidth=imageSize[0],
                ditHeight=imageSize[1],
                isLabeled=ConstantUtils.IMAGE_UNLABEL
            ))

        classifyImageItem.objects.insert(saveImageItemList, load_bulk=False)
        # 更新数据集数量
        clssifyDatasetsService().updateDataSetStatisData(dsId)
        return resultPackerUtils.save_success()


    def saveMultiImages(self, desFolderBasePath, imageslist):
        # 新建该文件加，并保存图片
        imageNameList = []
        imagePathList = []
        os.mkdir(desFolderBasePath)
        for imageItem in imageslist:
            # orign name list
            imageNameList.append(imageItem.filename)
            # pack imagePathList
            savedImageName = fileUtils.getRandomName(imageItem.filename)
            imagePathList.append(savedImageName)
            # save image
            imageItem.save(desFolderBasePath + "/" + savedImageName)

        return imageNameList, imagePathList

    """
        保存压缩包数据
    """

    def saveCompressedFile(self, desFolderBasePath, compreImgPack):

        newFilePathName = desFolderBasePath + fileUtils.getFileSuffix(compreImgPack.filename)
        # save the file
        compreImgPack.save(newFilePathName);
        # extract files
        return fileUtils.extractFiles(newFilePathName, desFolderBasePath)

    """
        获取数据项item
    """

    def getImageItemList(self, pageItem, data):

        totalCount = dataImageItem.objects(__raw__={'dsId': data['dsId']},state=ConstantUtils.DATA_STATUS_ACTIVE).count()

        dataList = dataImageItem.objects(__raw__={'dsId': data['dsId']},state=ConstantUtils.DATA_STATUS_ACTIVE).skip(
            pageItem.skipIndex).limit(pageItem.pageSize)

        pageItem.set_totalCount(totalCount)


        #获取该数据集下所有的标签
        labelMap,nameList=labelService.getLabelsBylids(data['dsId'])

        dataArray = json.loads(dataList.to_json())
        for item in dataArray:
            item['ditFilePath'] = ConstantUtils.imageItemPrefix + item['ditFilePath'].replace("/","_")
            if item.keys().__contains__("recLabelList"):
                recLabelList=item['recLabelList']
                newList=[]
                for labelItem in recLabelList:
                    if labelMap.keys().__contains__(labelItem['dlid']):
                        labelItem['dlName']=labelMap[labelItem['dlid']]
                        newList.append(labelItem)
                item['recLabelList']=newList




        pageItem.set_numpy_dataList(dataArray)

        return resultPackerUtils.packPageResult(pageItem);


    def getImageItemDetail(self,queryData):
        imageItem= dataImageItem.objects(ditId=queryData['ditId'],state=ConstantUtils.DATA_STATUS_ACTIVE)[0]
        labelMap,nameList=labelService.getLabelsBylids(imageItem['dsId'])
        imageItem['ditFilePath'] = ConstantUtils.imageItemPrefix + imageItem['ditFilePath'].replace("/", "_")

        obj=json.loads(imageItem.to_json())
        recLabelList=obj['recLabelList']

        newList = []
        for labelItem in recLabelList:
            if labelMap.keys().__contains__(labelItem['dlid']):
                labelItem['dlName'] = labelMap[labelItem['dlid']]
                newList.append(labelItem)
        imageItem['recLabelList'] = newList

        return resultPackerUtils.packDataListResults(imageItem.to_json())


    def delImageItem(self,ditId):
        imageItem = dataImageItem.objects(ditId=ditId)
        imageItem.update(state=ConstantUtils.DATA_STATUS_DELETED)

        #更新数据集图片数量和标注进度
        print(imageItem[0]["dsId"])
        self.updateDataSetStatisData(imageItem[0]["dsId"])

        return resultPackerUtils.update_success()

    def updateDataSetStatisData(self,dsId):

        dsItem = datasetsBean.objects(dsId=dsId, state=ConstantUtils.DATA_STATUS_ACTIVE)[0]

        #更新总数量
        totalCount = dataImageItem.objects(dsId=dsId,state=1).count()

        labledCount = dataImageItem.objects(dsId=dsId,isLabeled=1, state=1).count()

        dsItem.update(dsImageCount=totalCount,dsImgTagSP=labledCount)



    """
        上传标注数据    
    """

    def upImageItemRecLabels(self, data):

        dataImage = dataImageItem.objects(ditId=data["ditId"]).first()

        jsons = data["recLabelList"]
        jsons=imageUtils.addYOLOCorrdinate(jsons)

        labelIdList = []

        recLabelList = []
        for item in jsons:
            dlid = item['dlid']
            if labelIdList.__contains__(dlid) == False:
                labelIdList.append(dlid)
            recLabelList.append(rectangleLabelBean.convertToBean(item))

        dataImage.update(recLabelList=recLabelList, labelIdList=labelIdList,isLabeled=1)

        self.updateDataSetStatisData(data['dsId'])
        return resultPackerUtils.update_success()

    # 根据训练版本勾选的数据集查出数据并组装
    def loadTrainData(self,dmtvid,ds_dl_list):

        imagePathList = []
        LabelsList = []
        imageShapeList = []

        dl_id_index_map = {}
        dlOrderedList = []
        dlIndex = 0

        for dsItem in ds_dl_list:
            if dsItem['isSelectAll'] == ConstantUtils.TRUE_TAG:
                datImageList = dataImageItem.objects(dsId=dsItem["dsId"], state=1)
            else:
                datImageList = dataImageItem.objects(dsId=dsItem["dsId"], labelIdList__in=dsItem["dlidList"], state=1)

            for imageItem in datImageList:

                reclabelList = imageItem['recLabelList']
                # 如果图片有标注数据，才参与训练
                if len(reclabelList) > 0:
                    itemLabelList = []
                    for item in reclabelList:
                        if (dsItem['isSelectAll'] == ConstantUtils.TRUE_TAG or
                                (dsItem['isSelectAll'] == ConstantUtils.FALSE_TAG and dsItem["dlidList"].__contains__(item['dlid']))):
                            if not dl_id_index_map.keys().__contains__(item['dlid']):
                                dl_id_index_map[item['dlid']]=dlIndex
                                dlOrderedList.append(item['dlid'])
                                dlIndex+=1

                            itemLabelList.append([dl_id_index_map[item['dlid']], item['rec_yolo_x'], item['rec_yolo_y'], item['rec_w'], item['rec_h']])

                    imagePathList.append(fileUtils.getABSPath(imageItem['ditFilePath']))
                    imageShapeList.append([imageItem['ditWidth'], imageItem['ditHeight']])
                    LabelsList.append(np.array(itemLabelList))
        print("***************dlid_dlIndex_map**************")
        print(str(dl_id_index_map))
        #将dlid和index的关系保存到trainVersion中
        detectModelTrainVersion.objects(dmtvid=dmtvid,state=ConstantUtils.DATA_STATUS_ACTIVE).update(dl_id_index_map=str(dl_id_index_map))
        labelMap, nameList = labelService.getLabelsBylids(dsItem["dsId"])
        #对nameList进行排序
        newnameList=[labelMap[item] for item in dlOrderedList]
        loggerUtils.info("labelMap:" + str(labelMap))
        index = 0
        for i in range(imagePathList.__len__()):
            print("-----------------****" + str(index) + "******-----------------")
            print(imagePathList[i])
            print(LabelsList[i])
            print(imageShapeList[i])
            index += 1

        trainDataDict = {
            "imagePathList": imagePathList,
            "LabelsList": np.array(LabelsList),
            "imageShapeList": np.array(imageShapeList),
            "nc": newnameList.__len__(),
            "names": newnameList
        }

        valDataDict = {
            "imagePathList": imagePathList,
            "LabelsList": np.array(LabelsList),
            "imageShapeList": np.array(imageShapeList),
            "nc": newnameList.__len__(),
            "names": newnameList
        }

        return trainDataDict, valDataDict

    def getAllCVTaskTypes(self):

        taskTypeList=[
            {
                "cvTaskType":ConstantUtils.CV_TASK_TYPE_CLASSIFY,
                "cvTaskName":ConstantUtils.getCVTaskTypaName(ConstantUtils.CV_TASK_TYPE_CLASSIFY)
            },
            {
                "cvTaskType": ConstantUtils.CV_TASK_TYPE_DETECT,
                "cvTaskName": ConstantUtils.getCVTaskTypaName(ConstantUtils.CV_TASK_TYPE_DETECT)
            }
        ]

        return resultPackerUtils.packCusResult({"taskTypeList":taskTypeList})





