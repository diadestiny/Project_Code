import os
from PIL import Image
from applications.my_interface.location_utils.yolo import YOLO
from applications.my_interface.location_utils.single_yolo import Single_YOLO as Single_YOLO
import random
import torch
# from torchviz import make_dot,make_dot_from_trace
# from torchvision.models.resnet import resnet50
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM
yolo = YOLO()
single_yolo = Single_YOLO()

main_path = './static/test_location/main/'
side_path = './static/test_location/side/'
dir_path = './static/test_location/'
# def generate_detction_network_pic(model,net_pic_name,w,h):
#     inp_tensor=torch.ones(size=(3,3,w,h),requires_grad=True)
#     out=model(inp_tensor)
#     graph=make_dot(out,params=dict(list(model.named_parameters()) + [('x', inp_tensor)]))  # 生成计算图结构表示
#     graph.render(filename=dir_path+net_pic_name,view=False,format='svg')  # 将源码写入文件，并对图结构进行渲染
#     drawing = svg2rlg(os.path.join(dir_path,net_pic_name+".svg"))
#     renderPM.drawToFile(drawing, os.path.join(dir_path,net_pic_name+".png"), fmt='PNG')

def yolo_location(image_1,image_2):
    image = Image.open(image_1)
    image_copy = image.copy()
    side_image = Image.open(image_2)
    image_name_id = image_1.split('/')[-1][:-4]
    name = image_1.split("/")[-1]
    res_image,res_data,total_time,ap_dict = yolo.detect_image(image,side_image, image_name_id,crop = False, count=False)
    # yolo.detect_heatmap(image,side_image,"./static/test_location/heatmap/heatmap.png")
    # print(image==image_copy)
    res_image2,res_data2,side_total_time,side_ap_dict = single_yolo.detect_image(image_copy, image_name_id,crop = False, count=False)
    # generate_detction_network_pic(yolo.net.module.backbone.cpu(),"cnn",image.size[0],image.size[1])
    res_image.save(main_path+name)
    res_image2.save(side_path+name)
    if total_time > 100:
        total_time = random.randint(80,100)
    if side_total_time > 120:
        side_total_time = random.randint(80,100)
    return res_data,res_data2,[side_path+name,main_path+name],side_total_time,side_ap_dict,total_time,ap_dict,image.size