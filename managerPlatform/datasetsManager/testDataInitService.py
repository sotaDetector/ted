import os

from managerPlatform.bean.trainDataset.dataImageItem import dataImageItem
from managerPlatform.bean.trainDataset.dataLabelBean import dataLabelBean
from managerPlatform.bean.trainDataset.rectangleLabelBean import rectangleLabelBean
from managerPlatform.common.commonUtils.imageUtils import imageUtils


class testDataInitService:


    def initLabels(self,dsId):

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
                      'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
                      'couch',
                      'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                      'keyboard',
                      'cell phone',
                      'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                      'teddy bear',
                      'hair drier', 'toothbrush']
        LabelList = []
        for i in range(0, len(labelArray)):
            LabelList.append(dataLabelBean(
                dlName=labelArray[i],
                dsId=dsId
            ))

        dataLabelBean.objects.insert(LabelList, load_bulk=False)

        dataLabelsList=dataLabelBean.objects(dsId=dsId,state=1)

        dl_name_id_map={}
        for item in dataLabelsList:
            dl_name_id_map[item['dlName']]=item['dlid']


        dl_index_id_map={}
        for i in range(0, len(labelArray)):
            dl_index_id_map[i]=dl_name_id_map[labelArray[i]]


        print("-----dl_index_id_map-----")
        print(dl_index_id_map)
        return dl_index_id_map







    def initImageLabeldData(self,dsId,labelMap):
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
                    rec_yolo_x=dataItem[1],
                    rec_yolo_y=dataItem[2],
                    rec_w=dataItem[3],
                    rec_h=dataItem[4],
                    dlid=labelMap[int(labelId)]
                ))

            imageItemList.append(dataImageItem(
                ditFileName=i.replace(".txt", ".jpg"),
                ditFilePath="train_test/" + i.replace(".txt", ".jpg"),
                ditWidth=imageSize[0],
                ditHeight=imageSize[1],
                dsId=dsId,
                recLabelList=recLabelList,
                labelIdList=labelIdList
            ))
        dataImageItem.objects.insert(imageItemList, load_bulk=False)



    def initTrainModelDataSet(self,data):
        dsId=data['dsId']
        labelMap=self.initLabels(dsId)

        self.initImageLabeldData(dsId,labelMap)


        return {"rs": 1, "dsId":dsId}
