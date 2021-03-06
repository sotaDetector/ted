import argparse
import threading
import time
from pathlib import Path
import os
from queue import Queue

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from managerPlatform.common.commonUtils.randomUtils import randomUtils
from managerPlatform.common.commonUtils.videoRecordUtils import videoRecordUtils
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, \
    strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class detectServiceThread(threading.Thread):

    # 创建流队列
    def createStreamQueue(self):
        self.q = Queue(maxsize=0)

    # 获取流队列
    def getStreamQueue(self):
        return self.q

    # 停止检测
    def stopDetect(self):
        self.isDetect = False
        if self.isStream:
            self.dataset.stopGrabStreamData()

    # 加载模型
    def loadModel(self, modelConfig):
        print("模型配置：" + str(modelConfig))
        # 设置设备类型
        self.device = select_device(modelConfig["device"])
        # 设置精度
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = attempt_load(modelConfig["weights"], map_location=self.device)  # load FP32 model

        if self.half:
            model.half()  # to FP16

        self.model = model

    # 加载配置参数
    def setDetectConfig(self, detectConfig):
        # 配置检测参数
        self.detectConfig = detectConfig

    # 创建线程时，运行该函数
    def run(self):

        with torch.no_grad():
            self.detect(self.detectConfig)


    def startBroardcast(self):
        self.Broardcast=True

    # 初始化一些参数 并加载模型
    def __init__(self, modelConfig):
        threading.Thread.__init__(self)
        set_logging()

        self.isStream = False

        #默认开启直播
        self.Broardcast=False

        # 是否继续检测 检测任务关闭时把该值设为false
        self.isDetect = True
        # 创建stream队列，用于传输图像信息
        self.createStreamQueue()

        # 加载模型
        self.loadModel(modelConfig)

    def detect(self, detetConfig=None):

        detectResult = []

        print("检测参数：" + str(detetConfig))
        model = self.model
        save_img = False
        vw = None
        # 初始化若干参数
        source, view_img, save_txt = detetConfig["source"], detetConfig["view_img"], detetConfig["save_txt"]

        webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
            ('rtsp://', 'rtmp://', 'http://'))

        # Directories
        save_dir = Path(detetConfig['saveDir'])  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        half = self.half
        device = self.device
        # 检查图像
        imgsz = check_img_size(detetConfig["imgsz"], s=model.stride.max())  # check img_size

        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

        # Set Dataloader
        vid_path, vid_writer = None, None
        if webcam:
            view_img = True
            cudnn.benchmark = True  # set True to speed up constant image size inference
            self.dataset = LoadStreams(source, img_size=imgsz)
            self.cap = self.dataset.getCap()
            self.isStream=True
            vw = videoRecordUtils.createVideoWriter(self.cap)
        else:
            save_img = True
            self.isStream = False
            self.dataset = LoadImages(source, img_size=imgsz)

        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once

        for path, img, im0s, vid_cap in self.dataset:
            if self.isDetect == False:
                break
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=detetConfig["augment"])[0]

            # Apply NMS
            pred = non_max_suppression(pred, detetConfig["conf_thres"], detetConfig["iou_thres"],
                                       classes=detetConfig["classes"],
                                       agnostic=detetConfig["agnostic_nms"])
            t2 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0 = Path(path[i]), '%g: ' % i, im0s[i].copy()
                else:
                    p, s, im0 = Path(path), '', im0s

                save_path = str(save_dir / p.name)
                txt_path = str(save_dir / 'labels' / p.stem) + (
                    '_%g' % self.dataset.frame if self.dataset.mode == 'video' else '')
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %ss, ' % (n, names[int(c)])  # add to string

                    # Write results
                    detectObjectItems = []
                    for *xyxy, conf, cls in reversed(det):

                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if detetConfig["save_conf"] else (cls, *xywh)  # label format
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        if save_img or view_img:  # Add bbox to image
                            label = '%s %.2f' % (names[int(cls)], conf)
                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                            detectObjectItems.append({
                                "x": int(xyxy[0]),
                                "y": int(xyxy[1]),
                                "w": int(xyxy[2]),
                                "h": int(xyxy[3]),
                                "label": label,
                                "class": int(cls.int()),
                                "conf": float(conf.float()),
                                "color":colors[int(cls)]
                            })

                    detectResult.append({
                        "file": p.name,
                        "detectObject": detectObjectItems
                    })

                # Print time (inference + NMS)
                print('%sDone. (%.3fs)' % (s, t2 - t1))

                # Stream results
                if view_img:
                    ret, buffer = cv2.imencode('.jpg', im0)
                    frame = buffer.tobytes()
                    # record video
                    print("record video....")
                    vw.write(im0)
                    if self.Broardcast:
                        #为节省内存资源 如果队列数量超过 30则清空
                        if self.q.qsize()>30:
                            self.q.queue.clear()
                        self.q.put(frame)

                # Save results (image with detections)
                if save_img:
                    if self.dataset.mode == 'images':
                        cv2.imwrite(save_path, im0)
                    else:
                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()  # release previous video writer

                            fourcc = 'mp4v'  # output video codec
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                        vid_writer.write(im0)

        if vw != None:
            pass
            videoRecordUtils.closeVideoWrite(vw)


        print("detect finished.......")

        return detectResult
