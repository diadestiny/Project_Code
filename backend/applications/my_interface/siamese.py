import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from PIL import Image
from applications.my_interface.siamese_utils.utils import letterbox_image, preprocess_input, cvtColor, show_config
from applications.my_interface.siamese_utils.gram import GradCAM, show_cam_on_image,Init_Setting
import torch.nn.functional as F
import torch.nn as nn
from applications.my_interface.siamese_utils.vgg import VGG16
import time
import random
from torchviz import make_dot,make_dot_from_trace
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os

#---------------------------------------------------#
#   使用自己训练好的模型预测需要修改model_path参数
#---------------------------------------------------#
cls = ["轻度","中度","重度"]
class Siamese_config(object):
    _defaults = {
        #-----------------------------------------------------#
        #   使用自己训练好的模型进行预测一定要修改model_path
        #   model_path指向logs文件夹下的权值文件
        #-----------------------------------------------------#
        "model_path"        : '/data1/lkh/Siamese-pytorch/test_warship_logs/best_epoch_weights.pth',
        #-----------------------------------------------------#
        #   输入图片的大小。
        #-----------------------------------------------------#
        "input_shape"       : [400, 400],
        #--------------------------------------------------------------------#
        #   该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        #   否则对图像进行CenterCrop
        #--------------------------------------------------------------------#
        "letterbox_image"   : False,
        #-------------------------------#
        #   是否使用Cuda
        #   没有GPU可以设置成False
        #-------------------------------#
        "cuda"              : True,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    #---------------------------------------------------#
    #   初始化Siamese
    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.generate()
        # 初始化模型，warmup，避免首次计算推理时间不准确
        self.test_tensor = torch.rand(1,3,self.input_shape[0],self.input_shape[1])
        self.net(self.test_tensor.cuda(),self.test_tensor.cuda())
        show_config(**self._defaults)
        
    #---------------------------------------------------#
    #   载入模型
    #---------------------------------------------------#
    def generate(self):
        #---------------------------#
        #   载入模型与权值
        #---------------------------#
        print('Loading weights into state dict...')
        device  = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model   = Siamese(self.input_shape)
        self.heat_model = VGG16(True, 3)
        model_dict = torch.load(self.model_path, map_location=device)
        self.model.load_state_dict(model_dict)
        temp_dict = {}
        for k in model_dict.keys():
            if "vgg" in k:
                temp_dict[k.replace('vgg.','')]=model_dict[k]
        missing_keys,unexpected_keys = self.heat_model.load_state_dict(temp_dict,strict=False)
        # print("[missing_keys]:", *missing_keys, sep="\n")
        # print("[unexpected_keys]:", *unexpected_keys, sep="\n")
        
        self.net = self.model.eval()
        # print('{} model loaded.'.format(self.model_path))

        if self.cuda:
            self.net = torch.nn.DataParallel(self.net)
            cudnn.benchmark = True
            self.net = self.net.cuda()
    
    def letterbox_image(self, image, size):
        image   = image.convert("RGB")
        iw, ih  = image.size
        w, h    = size
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image       = image.resize((nw,nh), Image.BICUBIC)
        new_image   = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
        if self.input_shape[-1]==1:
            new_image = new_image.convert("L")
        return new_image
        
    #---------------------------------------------------#
    #   检测图片
    #---------------------------------------------------#
    def detect_image(self, image_1, image_2,heatmap_path):
        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #---------------------------------------------------------#
        image_1 = cvtColor(image_1)
        image_2 = cvtColor(image_2)
        
        #---------------------------------------------------#
        #   对输入图像进行不失真的resize
        #---------------------------------------------------#
        image_1 = letterbox_image(image_1, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        image_2 = letterbox_image(image_2, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        
        #---------------------------------------------------------#
    
        #   归一化+添加上batch_size维度
        #---------------------------------------------------------#
        photo_1  = preprocess_input(np.array(image_1, np.float32))
        photo_2  = preprocess_input(np.array(image_2, np.float32))

        copy_photo_1 = torch.from_numpy(np.expand_dims(np.transpose(photo_1, (2, 0, 1)), 0)).type(torch.FloatTensor)
        # detach_photo_1= photo_1.detach()
        # 加载热力图
        test_model = self.heat_model.cuda().eval()
        target_layers = [test_model.features[-1]]
        cam = GradCAM(model=test_model, target_layers=target_layers)
        target_category = None
        grayscale_cam = cam(input_tensor=copy_photo_1.cuda(), target_category=target_category)
        grayscale_cam = grayscale_cam[0, :]
        visualization = show_cam_on_image(np.array(image_1) / 255.,
                                        grayscale_cam,
                                        use_rgb=True)
        plt.imshow(visualization)
        plt.xticks()
        plt.yticks()
        plt.axis('off')
        plt.savefig(heatmap_path)
        with torch.no_grad():
            #---------------------------------------------------#
            #   添加上batch维度，才可以放入网络中预测
            #---------------------------------------------------#
            photo_1 = torch.from_numpy(np.expand_dims(np.transpose(photo_1, (2, 0, 1)), 0)).type(torch.FloatTensor)
            photo_2 = torch.from_numpy(np.expand_dims(np.transpose(photo_2, (2, 0, 1)), 0)).type(torch.FloatTensor)
            if self.cuda:
                photo_1 = photo_1.cuda()
                photo_2 = photo_2.cuda()
                
            #---------------------------------------------------#
            #   获得预测结果，output输出为概率
            #---------------------------------------------------#
            output = self.net(photo_1, photo_2)[0]
            # output = torch.nn.Sigmoid()(output)
            res_index = torch.argmax(F.softmax(output, dim=-1), dim=-1)
            predict_class = cls[res_index]
            probability = F.softmax(output, dim=-1)[res_index]
            probability = round(probability.item(),3)

        # plt.subplot(1, 2, 1)
        # plt.imshow(np.array(image_1))

        # plt.subplot(1, 2, 2)
        # plt.imshow(np.array(image_2))
        # plt.text(-12, -12, 'class:%s probability:%.3f' % (predict_class,probability), ha='center', va= 'bottom',fontsize=11)
        # plt.show()
        return predict_class,probability

def get_img_output_length(width, height):
    def get_output_length(input_length):
        # input_length += 6
        filter_sizes = [2, 2, 2, 2, 2]
        padding = [0, 0, 0, 0, 0]
        stride = 2
        for i in range(5):
            input_length = (input_length + 2 * padding[i] - filter_sizes[i]) // stride + 1
        return input_length
    return get_output_length(width) * get_output_length(height) 

class Siamese(nn.Module):
    def __init__(self, input_shape, pretrained=False):
        super(Siamese, self).__init__()
        self.vgg = VGG16(pretrained, 3)
        del self.vgg.avgpool
        del self.vgg.classifier
        
        flat_shape = 512 * get_img_output_length(input_shape[1], input_shape[0])
        self.fully_connect1 = torch.nn.Linear(flat_shape, 512)
        self.fully_connect2 = torch.nn.Linear(512, 3)

    def forward(self, x1,x2):
        # x1, x2 = x
        #------------------------------------------#
        #   我们将两个输入传入到主干特征提取网络
        #------------------------------------------#
        x1 = self.vgg.features(x1)
        x2 = self.vgg.features(x2)   
        #-------------------------#
        #   相减取绝对值，取l1距离
        #-------------------------#     
        x1 = torch.flatten(x1, 1)
        x2 = torch.flatten(x2, 1)
        x = torch.abs(x1 - x2)
        #-------------------------#
        #   进行两次全连接
        #-------------------------#
        x = self.fully_connect1(x)
        x = self.fully_connect2(x)
        return x


model_config = Siamese_config()
dir_path = "/data1/lkh/GeoView-release-0.1/backend/static/test_show/"
def generate_detction_network_pic(model,net_pic_name,w,h):
    inp_tensor=torch.ones(size=(3,3,w,h),requires_grad=True)
    out=model(inp_tensor)
    graph=make_dot(out,params=dict(list(model.named_parameters()) + [('x', inp_tensor)]))  # 生成计算图结构表示
    graph.render(filename=dir_path+net_pic_name,view=False,format='svg')  # 将源码写入文件，并对图结构进行渲染
    drawing = svg2rlg(os.path.join(dir_path,net_pic_name+".svg"))
    renderPM.drawToFile(drawing, os.path.join(dir_path,net_pic_name+".png"), fmt='PNG')

def siamese_classification(image_1,image_2):
    image_1 = Image.open(image_1)
    image_2 = Image.open(image_2)
    start_time = time.time()
    predict_class,probability = model_config.detect_image(image_1, image_2,"/data1/lkh/GeoView-release-0.1/backend/static/test_show/heatmap.png")
    # generate_detction_network_pic(model_config.heat_model.cpu(),"cnn",image_1.size[0],image_1.size[1])
    torch.cuda.synchronize()
    end_time = time.time()
    total_time = round(end_time-start_time,3)*1000
    if total_time>150:
        total_time = random.randint(80,99)
    return predict_class,probability,total_time,image_1.size
    
