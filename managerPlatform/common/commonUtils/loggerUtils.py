import logging

from managerPlatform.common.config.configUtils import configUtils


class loggerUtils:

    clevel = logging.DEBUG
    Flevel = logging.INFO

    logger = logging.getLogger("serviceLog")
    logger.setLevel(clevel)
    fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    # 设置CMD日志
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(clevel)
    # 设置文件日志
    fh = logging.FileHandler(configUtils.getConfigProperties("log","log_path"), encoding='utf-8')
    fh.setFormatter(fmt)
    fh.setLevel(Flevel)
    #设置输出handler
    logger.addHandler(sh)
    logger.addHandler(fh)


    @classmethod
    def info(cls, message):
        cls.logger.info(message)
