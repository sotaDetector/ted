from managerPlatform.bean.detectModel.detectModelTrainStatistics import detectModelTrainStatistics
from managerPlatform.common.commonUtils.ConstantUtils import ConstantUtils
from managerPlatform.common.commonUtils.resultPackerUtils import resultPackerUtils


class dmTrainStatisService:


    def getTrainStatistics(self,queryData):
        dataList=detectModelTrainStatistics.objects(dmtvid=queryData["dmtvid"],state=ConstantUtils.DATA_STATUS_ACTIVE)
        metrics_mAP_5,metrics_mAP,metrics_precision,metrics_recall=[],[],[],[]
        train_box_loss,train_cls_loss,train_obj_loss=[],[],[]
        val_box_loss, val_cls_loss,val_obj_loss=[],[],[]
        x_lr0,x_lr1,x_lr2=[],[],[]
        for item in dataList:
            metrics_mAP_5.append(item['metrics_mAP_5'])
            metrics_mAP.append(item['metrics_mAP'])
            metrics_precision.append(item['metrics_precision'])
            metrics_recall.append(item['metrics_recall'])
            train_box_loss.append(item['train_box_loss'])
            train_cls_loss.append(item['train_cls_loss'])
            train_obj_loss.append(item['train_obj_loss'])
            val_box_loss.append(item['val_box_loss'])
            val_cls_loss.append(item['val_cls_loss'])
            val_obj_loss.append(item['val_obj_loss'])
            x_lr0.append(item['x_lr0'])
            x_lr1.append(item['x_lr1'])
            x_lr2.append(item['x_lr2'])

        resultMap={
            "metrics_mAP_5":metrics_mAP_5,
            "metrics_mAP":metrics_mAP,
            "metrics_precision":metrics_precision,
            "metrics_recall":metrics_recall,
            "train_box_loss":train_box_loss,
            "train_cls_loss":train_cls_loss,
            "train_obj_loss":train_obj_loss,
            "val_box_loss":val_box_loss,
            "val_cls_loss":val_cls_loss,
            "val_obj_loss":val_obj_loss,
            "x_lr0":x_lr0,
            "x_lr1":x_lr1,
            "x_lr2":x_lr2
        }

        return resultPackerUtils.packCusResult(resultMap)


    def saveModelTrainStatis(self,statisMap):
        statisItem=detectModelTrainStatistics(
            dmtvid=statisMap['dmtvid'],
            epoch=statisMap['epoch'],
            metrics_mAP_5=statisMap['metrics/mAP_0.5'],
            metrics_mAP=statisMap['metrics/mAP_0.5:0.95'],
            metrics_precision=statisMap['metrics/precision'],
            metrics_recall=statisMap['metrics/recall'],
            train_box_loss=statisMap['train/box_loss'],
            train_cls_loss=statisMap['train/cls_loss'],
            train_obj_loss=statisMap['train/obj_loss'],
            val_box_loss=statisMap['val/box_loss'],
            val_cls_loss=statisMap['val/cls_loss'],
            val_obj_loss=statisMap['val/obj_loss'],
            x_lr0=statisMap['x/lr0'],
            x_lr1=statisMap['x/lr1'],
            x_lr2=statisMap['x/lr2']
        )
        statisItem.save()