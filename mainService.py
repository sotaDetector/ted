from flask import Flask, redirect, url_for, session, render_template,make_response
from managerPlatform.common.config.configUtils import configUtils
from managerPlatform.common.dataManager.mongoSource import mongoSource
from managerPlatform.common.resourceInit.appResourceManager import appResourceManager
from managerPlatform.common.watcherMangaer.detectThreadWatcher import detectThreadWatcher
from managerPlatform.dataLabel.dataLabelDispacher import dataLabel_blp
from managerPlatform.datasetsManager.datasetsDispacher import *
from managerPlatform.datasetsManager.testDataInitDispacher import test_data_init_blp
from managerPlatform.detectService.detectServiceCallerDispacher import dts_caller_blp
from managerPlatform.detectService.detectServiceManagerDiapacher import dts_blp
from managerPlatform.detectModelManager.detectModelDispacher import *
from managerPlatform.detectModelManager.detectModelTrainDispacher import detect_model_train_blp
from managerPlatform.detectModelManager.dmTrainStatisDispacher import dm_train_statis_blp
from managerPlatform.detectModelValidation.cameraStreamDispacher import camera_stream_val_blp
from managerPlatform.detectModelValidation.detValServiceDispacher import detect_service_blp
from managerPlatform.detectModelValidation.videoDetectDispacher import video_detect_blp
from managerPlatform.streamPlayerService.mediaPlayerDispacher import media_Player_blp
from managerPlatform.userManager.userManagerDispacher import user_manager_blp
from managerPlatform.detectModelValidation.imageDetectDispacher import iamge_detect_blp
from flask_cors import *
app = Flask(__name__, static_folder='resources', static_url_path='/resources')
app.register_blueprint(test_data_init_blp)
app.register_blueprint(dsm_blp)
app.register_blueprint(detect_model_blp)
app.register_blueprint(dataLabel_blp)
app.register_blueprint(detect_model_train_blp)
app.register_blueprint(camera_stream_val_blp)
app.register_blueprint(user_manager_blp)
app.register_blueprint(iamge_detect_blp)
app.register_blueprint(detect_service_blp)
app.register_blueprint(dm_train_statis_blp)
app.register_blueprint(video_detect_blp)
app.register_blueprint(dts_blp)
app.register_blueprint(media_Player_blp)
app.register_blueprint(dts_caller_blp)

app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.config["SESSION_COOKIE_HTTPONLY"]=False

CORS(app,supports_credentials=True,resources=r'/*')

appResource=appResourceManager()

mongoSource.initMongoDBSource(app)

#app全局资源初始化
appResource.resourceInit()
# #启动监控线程
# detectThread=detectThreadWatcher()
# detectThread.start()

@app.before_request
def appInterceptor():
    unInterceptPath=["login","userLogin","userRegister","index.html",".js",".css",".jpg",".png"]
    for item in unInterceptPath:
        if request.path.__contains__(item):
            return
    if session.get("userId")==None:
        return redirect(url_for('login'))
    else:
        return


@app.route("/login")
def login():
    return app.send_static_file("mark_img/ted/index.html")


print("service start successful...")
print(configUtils.getConfigProperties("service", "service_ip"))
app.run(host=configUtils.getConfigProperties("service", "service_host"),
        port=configUtils.getConfigProperties("service", "service_ip"))
print("service start...")

