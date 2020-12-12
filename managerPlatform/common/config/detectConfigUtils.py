class detectConfigUtils:
    @classmethod
    def getBasicDetectConfig(cls, source):
        detectConfig = {}
        detectConfig['source'] = source
        detectConfig['update'] = False  # action='store_true', help='update all models'
        detectConfig['device'] = ''  # default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu'
        detectConfig['imgsz'] = 640
        detectConfig['save_img'] = False
        detectConfig['view_img'] = False  # display results
        detectConfig['save_txt'] = False  # save results to *.txt
        detectConfig['saveDir'] = "/Volumes/study/objectDetection/ted/runs/detect/test"  #
        detectConfig['conf_thres'] = 0.25  # default=0.25, help='object confidence threshold'
        detectConfig['iou_thres'] = 0.45  # type=float, default=0.45, help='IOU threshold for NMS'
        detectConfig['classes'] = ""  # nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3'
        detectConfig['agnostic_nms'] = False  # action='store_true', help='class-agnostic NMS'
        detectConfig['augment'] = False  # action='store_true', help='augmented inference'
        detectConfig['save_conf'] = False  # action='store_true', help='save confidences in --save-txt labels'
        return detectConfig
