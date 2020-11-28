"""File for accessing YOLOv5 via PyTorch Hub https://pytorch.org/hub/

Usage:
    import torch
    detectModel = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, channels=3, classes=80)
"""

from pathlib import Path

import torch

from models.yolo import Model
from utils.general import set_logging
from utils.google_utils import attempt_download

dependencies = ['torch', 'yaml']
set_logging()


def create(name, pretrained, channels, classes):
    """Creates a specified YOLOv5 detectModel

    Arguments:
        name (str): name of detectModel, i.e. 'yolov5s'
        pretrained (bool): load pretrained weights into the detectModel
        channels (int): number of input channels
        classes (int): number of detectModel classes

    Returns:
        pytorch detectModel
    """
    config = Path(__file__).parent / 'models' / f'{name}.yaml'  # detectModel.yaml path
    try:
        model = Model(config, channels, classes)
        if pretrained:
            fname = f'{name}.pt'  # checkpoint filename
            attempt_download(fname)  # download if not found locally
            ckpt = torch.load(fname, map_location=torch.device('cpu'))  # load
            state_dict = ckpt['detectModel'].float().state_dict()  # to FP32
            state_dict = {k: v for k, v in state_dict.items() if model.state_dict()[k].shape == v.shape}  # filter
            model.load_state_dict(state_dict, strict=False)  # load
            if len(ckpt['detectModel'].names) == classes:
                model.names = ckpt['detectModel'].names  # set class names attribute
            # detectModel = detectModel.autoshape()  # for PIL/cv2/np inputs and NMS
        return model

    except Exception as e:
        help_url = 'https://github.com/ultralytics/yolov5/issues/36'
        s = 'Cache maybe be out of date, try force_reload=True. See %s for help.' % help_url
        raise Exception(s) from e


def yolov5s(pretrained=False, channels=3, classes=80):
    """YOLOv5-small detectModel from https://github.com/ultralytics/yolov5

    Arguments:
        pretrained (bool): load pretrained weights into the detectModel, default=False
        channels (int): number of input channels, default=3
        classes (int): number of detectModel classes, default=80

    Returns:
        pytorch detectModel
    """
    return create('yolov5s', pretrained, channels, classes)


def yolov5m(pretrained=False, channels=3, classes=80):
    """YOLOv5-medium detectModel from https://github.com/ultralytics/yolov5

    Arguments:
        pretrained (bool): load pretrained weights into the detectModel, default=False
        channels (int): number of input channels, default=3
        classes (int): number of detectModel classes, default=80

    Returns:
        pytorch detectModel
    """
    return create('yolov5m', pretrained, channels, classes)


def yolov5l(pretrained=False, channels=3, classes=80):
    """YOLOv5-large detectModel from https://github.com/ultralytics/yolov5

    Arguments:
        pretrained (bool): load pretrained weights into the detectModel, default=False
        channels (int): number of input channels, default=3
        classes (int): number of detectModel classes, default=80

    Returns:
        pytorch detectModel
    """
    return create('yolov5l', pretrained, channels, classes)


def yolov5x(pretrained=False, channels=3, classes=80):
    """YOLOv5-xlarge detectModel from https://github.com/ultralytics/yolov5

    Arguments:
        pretrained (bool): load pretrained weights into the detectModel, default=False
        channels (int): number of input channels, default=3
        classes (int): number of detectModel classes, default=80

    Returns:
        pytorch detectModel
    """
    return create('yolov5x', pretrained, channels, classes)


if __name__ == '__main__':
    model = create(name='yolov5s', pretrained=True, channels=3, classes=80)  # example
    model = model.fuse().autoshape()  # for PIL/cv2/np inputs and NMS

    # Verify inference
    from PIL import Image

    imgs = [Image.open(x) for x in Path('data/images').glob('*.jpg')]
    results = model(imgs)
    results.show()
    results.print()
