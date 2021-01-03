import uuid
import zipfile
import os

from managerPlatform.common.config.configUtils import configUtils


class fileUtils:

    compreImgPackPath = configUtils.getConfigProperties("file", "compreImgPackPath")

    """
        解压文件
    """
    @staticmethod
    def extractFiles(orignFile, DesFolder):

        imageNameList = []
        imagePathList = []
        # 对文件进行解压
        zip_file = zipfile.ZipFile(orignFile)
        zipNameList = zip_file.namelist()
        for fileItem in zipNameList:
            if fileUtils.fileFilter(fileItem):
                zip_file.extract(fileItem, DesFolder)
                imageNameList.append(fileItem)
                newName = fileUtils.getRandomName(fileItem)
                imagePathList.append(newName)
                os.rename(DesFolder + "/" + fileItem, DesFolder +"/"+newName)
        zip_file.close()
        return imageNameList, imagePathList

    @staticmethod
    def fileFilter(fileItem):
        # 过滤掉mac系统生成的缓存文件
        if fileItem.find("__MACOSX") < 0:
            # 过滤掉非图片文件
            if fileItem.find(".jpg") > 0 or fileItem.find(".png") > 0:
                return True
        return False

    """
        获取随机文件名（文件后缀和传入的文件名称一致）
    """
    @staticmethod
    def getRandomName(fileName):
        return str(uuid.uuid4()) + fileUtils.getFileSuffix(fileName)

    @staticmethod
    def getFileSuffix(fileName):
        return fileName[fileName.index("."):]

    @classmethod
    def getABSPath(cls,filePath):
        return cls.compreImgPackPath+"/"+filePath

    @classmethod
    def detectPath(cls,filePath):
        if not os.path.exists(filePath):
            os.mkdir(filePath)

    @classmethod
    def getModelSavePath(cls,basePath,projectPath):
        projectPath=basePath + projectPath
        modelBasePath=projectPath+"/weights"

        if not os.path.exists(modelBasePath):
            os.makedirs(modelBasePath)

        return projectPath,modelBasePath+"/best.pt",modelBasePath+"/entireModel.pt"

    @classmethod
    def make_zip(cls,source_dir, output_filename):
        zipf = zipfile.ZipFile(output_filename, 'w')
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()

    @classmethod
    def createFolder(cls, folderPath):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)




