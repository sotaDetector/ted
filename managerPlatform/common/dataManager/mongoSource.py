from flask_mongoengine import MongoEngine

from managerPlatform.common.commonUtils.loggerUtils import loggerUtils
from managerPlatform.common.config.configUtils import configUtils


class mongoSource:

    loggerUtils.info("mongodb init...")
    mdb=MongoEngine()
    @classmethod
    def initMongoDBSource(cls,app):
        app.config['MONGODB_SETTINGS'] = {
            'db': 'admin',
            'host': configUtils.getConfigProperties("mongo","mongo_host"),
            'port': int(configUtils.getConfigProperties("mongo","mongo_port")),
            'username':configUtils.getConfigProperties("mongo","mongo_user"),
            'password':configUtils.getConfigProperties("mongo","mongo_pwd")
        }
        cls.mdb.init_app(app)


