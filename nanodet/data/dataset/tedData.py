import os
import torch
from cv2 import cv2
from torch.utils.data import Dataset
import numpy as np
from managerPlatform.bean.trainDataset.dataImageItem import dataImageItem
from nanodet.data.transform import Pipeline

class datasets_ted(Dataset):

    def __init__(self,dataList):
        self.dataList=dataList

    def __len__(self):
        return len(self.dataList)

    def __getitem__(self, idx):
        return self.dataList[idx]

class tedDatasetsPretreatment:

    def getRecValue(self,baseValue,per):
        return baseValue*per


    def labelImgRec(self,sourceUrl,desUrl,width,height,gt_bboxes):
        im = cv2.imread(sourceUrl)
        for item in gt_bboxes:
            l_point_x=int(item[0])
            l_point_y =int(item[1])


            r_point_x=int(item[2])
            r_point_y = int(item[3])

            cv2.rectangle(im, (l_point_x, l_point_y), (r_point_x, r_point_y),(255, 0, 0), 2)
        cv2.imwrite(desUrl,im)
        # plt.imshow(img_2)
        # plt.axis('off')
        # plt.show()

    def makeData(self):
        # 查寻数据
        resultList = []
        dataList = dataImageItem.objects(dsId=self.dsId, state=1)

        dl_id_index_map={}
        dlIndex=0
        dlOrderedList=[]

        for item in dataList:

            img_info = {
                'file_name': item['ditFileName'],
                'height': item['ditHeight'],
                'width': item['ditWidth'],
                'id': item['ditId']
            }

            image_path = os.path.join(self.imageBasePath, item["ditFilePath"])
            img = cv2.imread(image_path)

            gt_bboxes = []
            gt_labels = []
            for boxItem in item['recLabelList']:
                x=self.getRecValue(item['ditWidth'],boxItem['rec_lt_x'])
                y=self.getRecValue(item['ditHeight'],boxItem['rec_lt_y'])
                w=self.getRecValue(item['ditWidth'],boxItem['rec_w'])
                h=self.getRecValue(item['ditHeight'],boxItem['rec_h'])
                boxItemObj = [x,y,x+w,y+h]
                gt_bboxes.append(boxItemObj)
                if not dl_id_index_map.keys().__contains__(boxItem['dlid']):
                    dl_id_index_map[boxItem['dlid']] = dlIndex
                    dlOrderedList.append(boxItem['dlid'])
                    dlIndex += 1
                gt_labels.append(dl_id_index_map[boxItem['dlid']])


            if img is None:
                print('image {} read failed.'.format(image_path))
                raise FileNotFoundError('Cant load image! Please check image path!')

            meta = dict(img=img,
                        img_info=img_info,
                        gt_bboxes=np.array(gt_bboxes),
                        gt_labels=np.array(gt_labels))

            meta = self.pipeline(meta, self.input_size)
            meta['img'] = torch.from_numpy(meta['img'].transpose(2, 0, 1))

            resultList.append(meta)

        print("dl_id_index_map:")
        print(dl_id_index_map)
        print(dlOrderedList)
        return resultList

    def __init__(self,
                 dsId,
                 imageBasePath,
                 input_size,
                 pipeline,
                 keep_ratio=True):
        self.dsId=dsId
        self.input_size=input_size
        self.imageBasePath=imageBasePath
        self.pipeline = Pipeline(pipeline, keep_ratio)



