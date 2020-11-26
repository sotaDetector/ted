from flask import Flask

from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.dataLabel.dataLabelDispacher import dataLabel_blp
from managerPlatform.datasetsManager.datasetsDispacher import *
from managerPlatform.modelsManager.detectModelDispacher import *
from managerPlatform.modelsManager.detectModelTrainDispacher import detect_model_train_blp

print("service start...")
app = Flask(__name__, static_folder='resources', static_url_path='/resources')
app.register_blueprint(dsm_blp)
app.register_blueprint(detect_model_blp)
app.register_blueprint(dataLabel_blp)
app.register_blueprint(detect_model_train_blp)

app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
#
mongoSource.initMongoDBSource(app)

print("service start successful...")

app.run(host=configUtils.getConfigProperties("service", "service_host"),
        port=configUtils.getConfigProperties("service", "service_ip"))
