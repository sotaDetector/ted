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
            "rec_lt_x": 0.658478,
            "rec_lt_y": 0.592133,
            "rec_yolo_x": 0.5551601423487544,
            "rec_yolo_y": 0.47527431791221825,
            "rec_w": 0.13345195729537365,
            "rec_h": 0.03202846975088968
        }
    ]
    imageUtils.labelImgRec("girl.jpg","result.jpg",800,1200,cordinate)
    # orignCorrdinate=[ {
    #         "rec_lt_x": 0.4884341637010676,
    #         "rec_lt_y": 0.4592600830367734,
    #         "rec_w":0.13345195729537365,
    #         "rec_h": 0.03202846975088968,
    #         "dlid": 3
    #     }]
    # print(imageUtils.addYOLOCorrdinate(orignCorrdinate))

