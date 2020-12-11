from mongoengine import EmbeddedDocument

from managerPlatform.common.dataManager.mongoSource import mongoSource


class rectangleLabelBean(EmbeddedDocument):
    rlid = mongoSource.mdb.SequenceField(primary_key=True)
    #矩形左上角点 x
    rec_lt_x = mongoSource.mdb.FloatField(required=True)
    rec_yolo_x=mongoSource.mdb.FloatField(required=True)
    # 矩形左上角点 y
    rec_lt_y = mongoSource.mdb.FloatField(required=True)
    rec_yolo_y=mongoSource.mdb.FloatField(required=True)
    # 矩形左上角点 width
    rec_w = mongoSource.mdb.FloatField(required=True)
    # 矩形左上角点 heiht
    rec_h = mongoSource.mdb.FloatField(required=True)
    # 标签id
    dlid = mongoSource.mdb.LongField(required=True)

    @staticmethod
    def convertToBean(jsonData):
        return rectangleLabelBean(
            rec_lt_x=jsonData['rec_lt_x'],
            rec_yolo_x=jsonData['rec_yolo_x'],
            rec_lt_y=jsonData['rec_lt_y'],
            rec_yolo_y=jsonData['rec_yolo_y'],
            rec_w=jsonData['rec_w'],
            rec_h=jsonData['rec_h'],
            dlid=jsonData['dlid']
        )
