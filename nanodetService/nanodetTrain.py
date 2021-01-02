import os
import threading

import torch
import argparse
import numpy as np
import torch.distributed as dist
from nanodet.util import mkdir, Logger, cfg, load_config
from nanodet.trainer import build_trainer
from nanodet.data.collate import collate_function
from nanodet.data.dataset import build_dataset
from nanodet.model.arch import build_model
from nanodet.evaluator import build_evaluator

class nanodetTrainThread(threading.Thread):

    def init_seeds(seed=0):
        """
        manually set a random seed for numpy, torch and cuda
        :param seed: random seed
        """
        torch.manual_seed(seed)
        np.random.seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        if seed == 0:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False

    def __init__(self,nanoTrainConfig):
        threading.Thread.__init__(self)
        self.nanoTrainConfig=nanoTrainConfig


    def run(self):
        self.startNanodetTrain()

    def startNanodetTrain(self):
        #加载配置文件
        load_config(cfg, self.nanoTrainConfig['cfg'])
        #判断分布式训练当中该主机的角色
        local_rank = int(self.nanoTrainConfig["local_rank"])
        # torch.backends.cudnn.enabled = True
        # torch.backends.cudnn.benchmark = True
        mkdir(local_rank, self.nanoTrainConfig["save_dir"])
        logger = Logger(local_rank, self.nanoTrainConfig["save_dir"])
        if self.nanoTrainConfig.keys().__contains__("seed"):
            logger.log('Set random seed to {}'.format(self.nanoTrainConfig['seed']))
            self.init_seeds(self.nanoTrainConfig['seed'])

        #1.创建模型
        model = build_model(cfg.model)
        model=model.cpu()

        #2.加载数据
        logger.log('Setting up data...')
        train_dataset = build_dataset(cfg.data.train, 'train',self.nanoTrainConfig)
        val_dataset = build_dataset(cfg.data.val, 'test',self.nanoTrainConfig)

        if len(cfg.device.gpu_ids) > 1:
            print('rank = ', local_rank)
            num_gpus = torch.cuda.device_count()
            torch.cuda.set_device(local_rank % num_gpus)
            dist.init_process_group(backend='nccl')
            train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
            train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=cfg.device.batchsize_per_gpu,
                                                           num_workers=cfg.device.workers_per_gpu, pin_memory=True,
                                                           collate_fn=collate_function, sampler=train_sampler,
                                                           drop_last=True)
        else:
            print("加载数据...")
            train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=cfg.device.batchsize_per_gpu,
                                                           shuffle=True, num_workers=cfg.device.workers_per_gpu,
                                                           pin_memory=True, collate_fn=collate_function, drop_last=True)

        val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=1, shuffle=False, num_workers=1,
                                                     pin_memory=True, collate_fn=collate_function, drop_last=True)

        trainer = build_trainer(local_rank, cfg, model, logger)

        if 'load_model' in cfg.schedule:
            trainer.load_model(cfg)
        if 'resume' in cfg.schedule:
            trainer.resume(cfg)

        evaluator = build_evaluator(cfg, val_dataset)

        logger.log('Starting training...')
        trainer.run(train_dataloader, val_dataloader, evaluator,self.nanoTrainConfig)


