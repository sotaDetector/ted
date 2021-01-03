import zipfile

import onnx
import torch
from onnxsim import simplify
import subprocess

from managerPlatform.common.commonUtils.fileUtils import fileUtils
from nanodet.model.arch import build_model
from nanodet.util import load_model_weight, load_config, cfg, Logger
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

#./onnx2ncnn /Volumes/study/objectDetection/nanodet/weights/handCheck.sim out.param out.bin

class liteModelConveter:

    #转化为手机端android模型
    def convertToNCNN_Android_model(self,config,model_path):

        modelBasePath = model_path[:model_path.rindex("/")]

        onnx_model=modelBasePath+"detect.onnx"
        sim_model=modelBasePath+"sim.onnx"
        androidModelPath=modelBasePath+"/androidModel"
        androidZIPFile=modelBasePath+"detect.zip"

        fileUtils.createFolder(androidModelPath)

        self.export_ONNX_model(config,model_path,onnx_model,Logger)
        self.simpfy_model(onnx_model,sim_model)

        self.convertToLiteModel(sim_model,androidModelPath,androidZIPFile)

        return androidZIPFile




    def export_ONNX_model(self,config,model_path,output_path,logger,input_shape=(320, 320)):
        model = build_model(config.model)
        checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)
        load_model_weight(model, checkpoint, logger)
        dummy_input = torch.autograd.Variable(torch.randn(1, 3, input_shape[0], input_shape[1]))
        torch.onnx.export(model, dummy_input, output_path, verbose=True, keep_initializers_as_inputs=True,
                          opset_version=11)

    #简化模型
    def simpfy_model(self,onnxModelPath,simModelOutPath):
        # load your predefined ONNX model
        model = onnx.load(onnxModelPath)

        # convert model
        model_simp, check = simplify(model)

        onnx.save(model_simp,simModelOutPath)


    def convertToLiteModel(self,simModelPath,androidModelPath,androidModelZIP):
        paramUrl=" "+androidModelPath+"/detect.param"
        binUrl=" "+androidModelPath+"/detect.bin"
        convertIns="/Volumes/study/objectDetection/ncnn/build/tools/onnx/onnx2ncnn "+simModelPath+paramUrl+binUrl
        result = subprocess.getstatusoutput(convertIns)

        fileUtils.make_zip(androidModelPath,androidModelZIP)
        #进行压缩
        print(result)


if __name__=="__main__":

    # cfg_path = r"../data/nanodet-self.yml"
    # model_path = r"../weights/mask_nanodet.pt"
    # onnx_out_path = r'../weights/mask_nanodet.onnx'
    # simpfy_out_path=r'../weights/mask_nanodet.sim'
    # load_config(cfg, cfg_path)
    #
    modelConveter=liteModelConveter()
    # modelConveter.convertToNCNN_Android_model(cfg,model_path,onnx_out_path,simpfy_out_path)

    modelConveter.make_zip("androidPath","androidPath.zip")

