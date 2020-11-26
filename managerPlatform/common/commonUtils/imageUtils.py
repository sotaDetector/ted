from PIL import Image
import PIL.ExifTags

class imageUtils:
    @staticmethod
    def getImageSize(imagePath):
        img = Image.open(imagePath)

        return img.size


if __name__=="__main__":
    print(imageUtils.getImageSize("/Volumes/study/hurtDetect/imgBase/faceImg/saveImg/081c51e0-be16-4dd5-84d9-40080cbe6771.jpg")[0])
