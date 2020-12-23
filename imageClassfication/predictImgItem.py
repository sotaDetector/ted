from __future__ import print_function, division
import numpy as np
from cv2 import cv2
from torchvision import datasets, models, transforms
#1.load the mode
import torch
from PIL import Image

#1. load the model
maskClassifyModel=torch.load("mask_train.pt")

maskClassifyModel.eval()


names=["mask","noMask"]

#2.read the

data_trans=transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

img=Image.open("0042.jpg")
img_tensor=data_trans(img)
print(type(img_tensor))
print(img_tensor.shape)
# transTensor=transforms.ToTensor()
# img_tensor=transTensor(img)
img_tensor=img_tensor[np.newaxis,:]

# print(img_tensor.shape)
#
#
result=maskClassifyModel(img_tensor)
print(result)
_, preds = torch.max(result, 1)
print(names[preds])