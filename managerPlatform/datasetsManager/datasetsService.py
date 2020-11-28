import os
import uuid
import numpy as np
from managerPlatform.bean.dataImageItem import dataImageItem
from managerPlatform.bean.datasetsBean import datasetsBean
from managerPlatform.bean.rectangleLabelBean import rectangleLabelBean
from managerPlatform.common.commonUtils.fileUtils import fileUtils
from managerPlatform.common.commonUtils.imageUtils import imageUtils
from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.dataLabel.dataLabelService import dataLabelService

compreImgPackPath = configUtils.getConfigProperties("file", "compreImgPackPath")
imageItemPrefix = configUtils.getConfigProperties("file", "imageItemPrefix")

labelService=dataLabelService()

class datasetsService:

    def addDataSet(self, dsName):

        dsName.save()

        return resultPackerUtils.save_success()

    def getDataSetPages(self, pageItem, dsName):

        totalCount = datasetsBean.objects().count()

        dataList = datasetsBean.objects(__raw__={'dsName': {'$regex': dsName}}).order_by('-create_date').skip(
            pageItem.skipIndex).exclude("state").limit(pageItem.pageSize)
        # only("dsName","dsType")
        pageItem.set_totalCount(totalCount)

        pageItem.set_dataList(dataList)

        return resultPackerUtils.packPageResult(pageItem);

    def upImageData(self, dsId, fileType, compreImgPack, imageslist):
        imageFiles = None

        folderName = str(uuid.uuid4())

        desFolderBasePath = compreImgPackPath + folderName

        if fileType == "1":
            imageNameList, imagePathList = self.saveCompressedFile(desFolderBasePath, compreImgPack)
        elif fileType == "2":
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

    def getImageItemList(self, dsId):

        return resultPackerUtils.packResults()

    """
        上传标注数据    
    """

    def upImageItemRecLabels(self, data):

        dataImage = dataImageItem.objects(ditId=data["ditId"]).first()

        jsons = data["recLabelList"]

        labelIdList = []

        recLabelList = []
        for item in jsons:
            dlid = item['dlid']
            if labelIdList.__contains__(dlid) == False:
                labelIdList.append(dlid)
            recLabelList.append(rectangleLabelBean.convertToBean(item))

        dataImage.update(recLabelList=recLabelList, labelIdList=labelIdList)

        return resultPackerUtils.update_success()

    # 根据训练版本勾选的数据集查出数据并组装
    def loadTrainData(self, ds_dl_list):

        imagePathList = []
        LabelsList = []
        imageShapeList = []
        nc = None
        names = []
        labelIndex = 0

        dlid_dlIndex_map = {}
        dlIndex_dlid_map = {}

        for dsItem in ds_dl_list:
            datImageList = dataImageItem.objects(dsId=dsItem["dsId"], labelIdList__in=dsItem["dlidList"])
            for item in datImageList:
                imagePathList.append(fileUtils.getABSPath(item['ditFilePath']))
                imageShapeList.append([item['ditWidth'], item['ditHeight']])
                reclabelList = item['recLabelList']
                itemLabelList = []
                for item in reclabelList:
                    if dsItem["dlidList"].__contains__(item['dlid']):
                        dlid = item['dlid']
                        if not dlid_dlIndex_map.keys().__contains__(dlid):
                            dlid_dlIndex_map[dlid] = labelIndex
                            dlIndex_dlid_map[labelIndex] = dlid
                            labelIndexValue=labelIndex
                            labelIndex += 1
                        else:
                            labelIndexValue = dlid_dlIndex_map[dlid]
                        itemLabelList.append(
                            [labelIndexValue, item['rec_lt_x'], item['rec_lt_y'], item['rec_w'], item['rec_h']])

                LabelsList.append(np.array(itemLabelList))
        print("***************dlid_dlIndex_map**************")
        labelMap=labelService.getLabelsBylids(dlid_dlIndex_map.keys())
        loggerUtils.info("labelMap:"+str(labelMap))
        for item in dlIndex_dlid_map.items():
            names.append(labelMap[item[1]])

        loggerUtils.info("label names:"+str(names))
        for i in range(imagePathList.__len__()):
            print("-----------------**********-----------------")
            print(imagePathList[i])
            print(LabelsList[i])
            print(imageShapeList[i])

        returlDict = {
            "imagePathList": imagePathList,
            "LabelsList": np.array(LabelsList),
            "imageShapeList": np.array(imageShapeList),
            "nc": names.__len__(),
            "names": names
        }

        return returlDict

    def initTestData(self):

        BasePath = "/Volumes/study/objectDetection/coco128/labels/train2017"
        imgBasePath = "/Volumes/study/objectDetection/coco128/images/train2017"
        allFiles = os.listdir(BasePath)
        imageItemList = []
        for i in allFiles:

            f = open(BasePath + "/" + i);  # 打开文件
            imageSize = imageUtils.getImageSize(imgBasePath + "/" + i.replace(".txt", ".jpg"))

            recLabelList = []
            labelIdList = []
            iter_f = iter(f);  # 创建迭代器

            for line in iter_f:
                dataItem = line.split(" ")
                labelId = dataItem[0]
                if labelIdList.__contains__(labelId) == False:
                    labelIdList.append(labelId)
                recLabelList.append(rectangleLabelBean(
                    rec_lt_x=dataItem[1],
                    rec_lt_y=dataItem[2],
                    rec_w=dataItem[3],
                    rec_h=dataItem[4],
                    dlid=labelId
                ))

            imageItemList.append(dataImageItem(
                ditFileName=i.replace(".txt", ".jpg"),
                ditFilePath="train_test/" + i.replace(".txt", ".jpg"),
                ditWidth=imageSize[0],
                ditHeight=imageSize[1],
                dsId=1,
                recLabelList=recLabelList,
                labelIdList=labelIdList
            ))
        dataImageItem.objects.insert(imageItemList, load_bulk=False)

        return {"rs": 1}
