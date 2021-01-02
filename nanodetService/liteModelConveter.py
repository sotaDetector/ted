import onnx
import torch
from onnxsim import simplify
import subprocess
from nanodet.model.arch import build_model
from nanodet.util import load_model_weight

#./onnx2ncnn /Volumes/study/objectDetection/nanodet/weights/handCheck.sim out.param out.bin

class liteModelConveter:

    #转化为手机端android模型
    def convertToNCNN_Android_model(self):
        pass




    # def export_ONNX_model(self):
    #     model = build_model(config.model)
    #     checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)
    #     load_model_weight(model, checkpoint, logger)
    #     dummy_input = torch.autograd.Variable(torch.randn(1, 3, input_shape[0], input_shape[1]))
    #     torch.onnx.export(model, dummy_input, output_path, verbose=True, keep_initializers_as_inputs=True,
    #                       opset_version=11)

    #简化模型
    def simpfy_model(self,onnxModelPath,simModelOutPath):
        # load your predefined ONNX model
        model = onnx.load(onnxModelPath)

        # convert model
        model_simp, check = simplify(model)

        onnx.save(model_simp,simModelOutPath)


    def convertToLiteModel(self):
        convertIns="/Volumes/study/objectDetection/ncnn/build/tools/onnx/onnx2ncnn /Volumes/study/objectDetection/nanodet/weights/handCheck.sim out.param out.bin"
        result = subprocess.getstatusoutput(convertIns)
        print(result)





if __name__=="__main__":
    modelConveter=liteModelConveter()
    modelConveter.convertToLiteModel()

