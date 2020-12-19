from managerPlatform.detectService.detectServiceManagerImpl import detectServiceImpl

detService=detectServiceImpl()
class appResourceManager:

    #app启动时初始化
    def resourceInit(self):
        #批量初始化检测模型
        detService.batchInitYoloModel()
