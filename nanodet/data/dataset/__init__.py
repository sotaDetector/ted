import copy
from .coco import CocoDataset
from .tedData import tedDatasetsPretreatment, datasets_ted
from .xml_dataset import XMLDataset

imageBasePath = "/Volumes/study/objectDetection/dataFactory/compressData/"



def build_dataset(cfg, mode,nanoTrainConfig):
    dataset_cfg = copy.deepcopy(cfg)
    name = dataset_cfg.pop('name')
    if name == 'coco':
        # return CocoDataset(mode=mode, **dataset_cfg)
        tedDSPre = tedDatasetsPretreatment(nanoTrainConfig['ds_dl_list'], imageBasePath=nanoTrainConfig['imageBasePath'],
                                        input_size=dataset_cfg.input_size,
                                        pipeline=dataset_cfg.pipeline,
                                        keep_ratio=dataset_cfg.keep_ratio)

        dataList = tedDSPre.dataPreprocess()

        return datasets_ted(dataList)

    if name == 'xml_dataset':
        return XMLDataset(mode=mode, **dataset_cfg)
    else:
        raise NotImplementedError('Unknown dataset type!')
