from datetime import datetime
import time

class dateUtils:

    @staticmethod
    def getNowDateTime():
        return datetime.now()

    @staticmethod
    def getTimeStamp():
        return int(round(time.time()*1000))


    