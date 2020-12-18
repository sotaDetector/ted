import cv2
import numpy
from PIL import Image
import matplotlib.pyplot as plt
import PIL.ExifTags

class imageUtils:
    @staticmethod
    def getImageSize(imagePath):
        img = Image.open(imagePath)

        return img.size

    @staticmethod
    def labelImgRec(sourceUrl,desUrl,width,height,yoloCorrdinates):
        im = cv2.imread(sourceUrl)
        for item in yoloCorrdinates:
            centerX=width*item["rec_yolo_x"]
            centery = height * item["rec_yolo_y"]
            objectWidth = width * item["rec_w"]
            objectHeight = height * item["rec_h"]

            halfWidth=objectWidth/2
            halfHeight=objectHeight/2
            l_point_x=int(centerX-halfWidth)
            l_point_y=int(centery-halfHeight)

            r_point_x=int(centerX+halfWidth)
            r_point_y = int(centery+halfHeight)

            cv2.rectangle(im, (l_point_x, l_point_y), (r_point_x, r_point_y),(255, 0, 0), 2)
        cv2.imwrite(desUrl,im)
        # plt.imshow(img_2)
        # plt.axis('off')
        # plt.show()

    @staticmethod
    def addYOLOCorrdinate(orignCoordinate):
        yoloFormat=[]
        for item in orignCoordinate:
            item['rec_yolo_x']=item['rec_lt_x']+item['rec_w']/2
            item['rec_yolo_y']=item['rec_lt_y']+item['rec_h']/2

            yoloFormat.append(item)
        return yoloFormat



if __name__=="__main__":
    cordinate= [
        {
            "rec_lt_x" : 0.16096381293402778,
            "rec_yolo_x" : 0.2609638129340278,
            "rec_lt_y" : 0.651797750721807,
            "rec_yolo_y" : 0.6873708732514513,
            "rec_w" : 0.2,
            "rec_h" : 0.07114624505928854,
        },
        {
            "rec_lt_x" : 0.1580008499710648,
            "rec_yolo_x" : 0.19874159071180555,
            "rec_lt_y" : 0.7901376716704237,
            "rec_yolo_y" : 0.8415210708799099,
            "rec_w" : 0.08148148148148149,
            "rec_h" : 0.10276679841897234,
        },
        {
            "rec_lt_x" : 0.7313341833043981,
            "rec_yolo_x" : 0.8276304796006945,
            "rec_lt_y" : 0.5450783831328743,
            "rec_yolo_y" : 0.584604074832479,
            "rec_w" : 0.1925925925925926,
            "rec_h" : 0.07905138339920949,
        },
        {
            "rec_lt_x" : 0.8454082573784722,
            "rec_yolo_x" : 0.8854082573784723,
            "rec_lt_y" : 0.7051574345162734,
            "rec_yolo_y" : 0.75950526060323,
            "rec_w" : 0.08,
            "rec_h" : 0.10869565217391304,
        },
        {
            "rec_lt_x" : 0.669111961082176,
            "rec_yolo_x" : 0.72318603515625,
            "rec_lt_y" : 0.7683985412356411,
            "rec_yolo_y" : 0.8326277902474988,
            "rec_w" : 0.10814814814814815,
            "rec_h" : 0.12845849802371542,
        },
        {
            "rec_lt_x" : 0.011334183304398148,
            "rec_yolo_x" : 0.03059344256365741,
            "rec_lt_y" : 0.6458688969668663,
            "rec_yolo_y" : 0.7357898455834672,
            "rec_w" : 0.03851851851851852,
            "rec_h" : 0.17984189723320157,
        }
    ]
    imageUtils.labelImgRec("84da5e84-3a59-4bf6-8072-f9158513a563_ba61ec28-34cd-4e83-ae67-60feab94af30.jpg",
                           "result.jpg",640,480,cordinate)
    # orignCorrdinate=[ {
    #         "rec_lt_x": 0.4884341637010676,
    #         "rec_lt_y": 0.4592600830367734,
    #         "rec_w":0.13345195729537365,
    #         "rec_h": 0.03202846975088968,
    #         "dlid": 3
    #     }]
    # print(imageUtils.addYOLOCorrdinate(orignCorrdinate))

