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
    def labelImgRec(width,height,corrdinate):
        im = cv2.imread("D://objectDetection/ted/data/train2017/000000000072.jpg")
        for item in corrdinate:
            centerX=width*item["rec_lt_x"]
            centery = height * item["rec_lt_y"]
            objectWidth = width * item["rec_w"]
            objectHeight = height * item["rec_h"]

            halfWidth=objectWidth/2
            halfHeight=objectHeight/2
            l_point_x=int(centerX-halfWidth)
            l_point_y=int(centery-halfHeight)

            r_point_x=int(centerX+halfWidth)
            r_point_y = int(centery+halfHeight)

            cv2.rectangle(im, (l_point_x, l_point_y), (r_point_x, r_point_y),(255, 0, 0), 2)
        plt.imshow(im)
        plt.axis('off')
        plt.show()


if __name__=="__main__":
    cordinate= [
        {
            "rec_lt_x": 0.658478,
            "rec_lt_y": 0.592133,
            "rec_w": 0.677002,
            "rec_h": 0.779766,
        },
        {
            "rec_lt_x": 0.391581,
            "rec_lt_y": 0.556305,
            "rec_w": 0.546862,
            "rec_h": 0.887391,
        }
    ]
    print(imageUtils.labelImgRec(427,640,cordinate))
