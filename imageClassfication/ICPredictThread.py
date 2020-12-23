import threading
import torch
import numpy as np
from torchvision import datasets, models, transforms
from PIL import Image
class ICTrainThread(threading.Thread):

    def __init__(self,modelPath):
        self.modelPath=modelPath


    #1.load the model
    def loadModel(self,modelPath):

        classifyModel = torch.load(modelPath)

        classifyModel.eval()

        self.classifyModel=classifyModel

    #2.classify the image
    def getClassifyResult(self,imagePath):
        data_trans = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        img_tensor = data_trans(Image.open(imagePath))

        img_tensor = img_tensor[np.newaxis, :]

        result = self.classifyModel(img_tensor)

        _, preds = torch.max(result, 1)

        print(preds)

    def run(self):
        threading.Thread.__init__(self)


if __name__=="__main__":
    