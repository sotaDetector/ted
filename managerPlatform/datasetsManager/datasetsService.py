import json
import os
import uuid
import numpy as np
from flask import session

from managerPlatform.bean.trainDataset.dataImageItem import dataImageItem
from managerPlatform.bean.trainDataset.dataLabelBean import dataLabelBean
from managerPlatform.bean.trainDataset.datasetsBean import datasetsBean
from managerPlatform.bean.trainDataset.rectangleLabelBean import rectangleLabelBean
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.imageUtils import imageUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.dataLabel.dataLabelService import dataLabelService



labelService = dataLabelService()


class datasetsService:

    def addDataSet(self, dsName):

        dsName.save()

        return resultPackerUtils.save_success()

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
                "labelList":labelList
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
        imageFiles = None

        folderName = str(uuid.uuid4())

        desFolderBasePath = ConstantUtils.dataBasePath + folderName

        imageNameList,imagePathList=None,None
        if fileType == ConstantUtils.UP_FILE_TYPE_COMPRESSFILE:
            imageNameList, imagePathList = self.saveCompressedFile(desFolderBasePath, compreImgPack)
        elif fileType == ConstantUtils.UP_FILE_TYPE_IMAGEFILE:
            imageNameList, imagePathList = self.saveMultiImages(desFolderBasePath, imageslist)

        # 保存到数据库
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
                ditHeight=imageSize[1]
            ))

        dataImageItem.objects.insert(saveImageItemList, load_bulk=False)
        #更新数据集数量
        self.updateDataSetStatisData(dsId['dsId'])
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
                for item in recLabelList:
                    item['dlName']=labelMap[item['dlid']]


        pageItem.set_numpy_dataList(dataArray)

        return resultPackerUtils.packPageResult(pageItem);


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
    def loadTrainData(self, ds_dl_list):

        imagePathList = []
        LabelsList = []
        imageShapeList = []


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
                            itemLabelList.append([item['dlid'], item['rec_lt_x'], item['rec_lt_y'], item['rec_w'], item['rec_h']])

                    imagePathList.append(fileUtils.getABSPath(imageItem['ditFilePath']))
                    imageShapeList.append([imageItem['ditWidth'], imageItem['ditHeight']])
                    LabelsList.append(np.array(itemLabelList))
        print("***************dlid_dlIndex_map**************")
        labelMap, nameList = labelService.getLabelsBylids(dsItem["dsId"])
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
            "nc": nameList.__len__(),
            "names": nameList
        }

        valDataDict = {
            "imagePathList": imagePathList,
            "LabelsList": np.array(LabelsList),
            "imageShapeList": np.array(imageShapeList),
            "nc": nameList.__len__(),
            "names": nameList
        }

        return trainDataDict, valDataDict

    def initTestData(self):

        # BasePath = "/Volumes/study/objectDetection/coco128/labels/train2017"
        # imgBasePath = "/Volumes/study/objectDetection/coco128/images/train2017"
        # allFiles = os.listdir(BasePath)
        # imageItemList = []
        # for i in allFiles:
        #
        #     f = open(BasePath + "/" + i);  # 打开文件
        #     imageSize = imageUtils.getImageSize(imgBasePath + "/" + i.replace(".txt", ".jpg"))
        #
        #     recLabelList = []
        #     labelIdList = []
        #     iter_f = iter(f);  # 创建迭代器
        #
        #     for line in iter_f:
        #         dataItem = line.split(" ")
        #         labelId = dataItem[0]
        #         if labelIdList.__contains__(labelId) == False:
        #             labelIdList.append(labelId)
        #         recLabelList.append(rectangleLabelBean(
        #             rec_lt_x=dataItem[1],
        #             rec_lt_y=dataItem[2],
        #             rec_w=dataItem[3],
        #             rec_h=dataItem[4],
        #             dlid=labelId
        #         ))
        #
        #     imageItemList.append(dataImageItem(
        #         ditFileName=i.replace(".txt", ".jpg"),
        #         ditFilePath="train_test/" + i.replace(".txt", ".jpg"),
        #         ditWidth=imageSize[0],
        #         ditHeight=imageSize[1],
        #         dsId=1,
        #         recLabelList=recLabelList,
        #         labelIdList=labelIdList
        #     ))
        # dataImageItem.objects.insert(imageItemList, load_bulk=False)

        # 初始化了labels
        labelArray = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                      'traffic light',
                      'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep',
                      'cow',
                      'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                      'frisbee',
                      'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                      'surfboard',
                      'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
                      'apple',
                      'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                      'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                      'cell phone',
                      'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                      'teddy bear',
                      'hair drier', 'toothbrush']
        LabelList = []
        for i in range(0, len(labelArray)):
            LabelList.append(dataLabelBean(
                dlIndex=i,
                dlName=labelArray[i],
                dsId=1
            ))

        dataLabelBean.objects.insert(LabelList, load_bulk=False)

        return {"rs": 1}
