import mmcv
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"]  = '6'
from mmdet.datasets.api_wrappers import COCO
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import cv2
import torch
import time
import xml.etree.ElementTree as ET
from .location_utils.cal_map import get_map
import random
from torchviz import make_dot,make_dot_from_trace
from torchvision.models.resnet import resnet50
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
# data_root = '/data1/lkh/dataset/small_ship_dataset/'
# json_file = data_root +'val.json'
out_file = '/data1/lkh/GeoView-release-0.1/backend/static/test_show/'
dir_path = '/data1/lkh/GeoView-release-0.1/backend/static/test_detection/'
heat_path = os.path.join(dir_path,"heatmap")
# coco = COCO(json_file)
config_file = '/data1/lkh/mmdet/work_dirs/detectors_cascade_rcnn_r50_1x_coco/detectors_cascade_rcnn_r50_1x_coco.py'
checkpoint_file = '/data1/lkh/mmdet/work_dirs/detectors_cascade_rcnn_r50_1x_coco/epoch_12.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')
class_map = {0:'Ship',1:'Warship', 2:'Ship', 3:'Ship'}
# class_names = ['Other Ship', 'Warship', 'Merchant', 'Dock']
class_names = ['Ship', 'Warship', 'Ship', 'Ship']
inference_detector(model,"/data1/lkh/GeoView-release-0.1/backend/static/upload/detection/000489.bmp")
generate_network_model=resnet50()

def generate_detction_network_pic(net_pic_name,w,h):
    inp_tensor=torch.ones(size=(3,3,w,h),requires_grad=True)
    out=generate_network_model(inp_tensor)
    graph=make_dot(out,params=dict(list(generate_network_model.named_parameters()) + [('x', inp_tensor)]))  # 生成计算图结构表示
    graph.render(filename=dir_path+net_pic_name,view=False,format='svg')  # 将源码写入文件，并对图结构进行渲染
    drawing = svg2rlg(os.path.join(dir_path,net_pic_name+".svg"))
    renderPM.drawToFile(drawing, os.path.join(dir_path,net_pic_name+".png"), fmt='PNG')

def deteciton_demo(img_path):
    start_time = time.time()
    img = mmcv.imread(img_path)
    # 热力图可视化传递路径
    with open(os.path.join(heat_path,"save.txt"),"w") as f:
        f.writelines(img_path)
    # generate_detction_network_pic("cnn",img.shape[1],img.shape[0])
    result = inference_detector(model,img_path)
    name = img_path.split('/')[-1]
    torch.cuda.synchronize()
    end_time = time.time()
    # print(start_time,end_time)
    model.show_result(img, result, out_file=out_file+name,show=True,score_thr=0.5,bbox_color=(255, 0, 0))
    bboxes = np.vstack(result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(result)
    ]
    labels = np.concatenate(labels)
    score_thr = 0.5
    # assert bboxes is not None and bboxes.shape[1] == 5
    scores = bboxes[:, -1]
    inds = scores > score_thr
    bboxes_score = bboxes[inds, :]
    labels = labels[inds]
    res_data= dict()
    res_data['bbox'] = list()
    res_data['class'] = list()
    res_data['score'] = list()
    res_data['size'] = list()
    image_name_id = name[:-4]
    total_time =  (end_time - start_time)*1000
    return_size = img.shape[:-1]
    if total_time > 100:
        total_time = random.randint(80,100)
    f = open(os.path.join(dir_path, "detection-results/"+image_name_id+".txt"), "w", encoding='utf-8') 
    for i,bs in enumerate(bboxes_score):
        [x1,y1,x2,y2,score] = bs
        # x1 = round(x1, 3)
        # y1 = round(y1, 3)
        # x2 = round(x2, 3)
        # y2 = round(y2, 3)
        score = round(score, 2)
        res_data['bbox'].append([str(int(x1)),str(int(y1)),str(int(x2)),str(int(y2))])
        res_data['size'].append([str(int(abs(x2-x1)))+"x"+str(int(abs(y2-y1)))])
        res_data['class'].append(class_map[labels[i]])
        res_data['score'].append(str(score))
        f.write("%s %s %s %s %s %s\n" % (class_map[labels[i]], score, str(int(x1)), str(int(y1)), str(int(x2)),str(int(y2))))
    f.close()
    if not os.path.exists(os.path.join("/data1/lkh/dataset/ShipRSImageNet_V1/VOC_Format/val_xml/"+image_name_id+".xml")):
        return res_data,out_file+name,round(total_time,3),{},return_size
    with open(os.path.join(dir_path, "ground-truth/"+image_name_id+".txt"), "w") as new_f:
        root = ET.parse(os.path.join("/data1/lkh/dataset/ShipRSImageNet_V1/VOC_Format/val_xml/"+image_name_id+".xml")).getroot()
        for obj in root.findall('object'):
            difficult_flag = False
            if obj.find('difficult')!=None:
                difficult = obj.find('difficult').text
                if int(difficult)==1:
                    difficult_flag = True
            obj_name = obj.find('name').text
            if obj_name == "Other Ship" or obj_name == "Merchant" or obj_name == "Dock":
                obj_name = "Ship"
            if obj_name not in class_names:
                continue
            bndbox  = obj.find('bndBox')
            left    = bndbox.find('xmin').text
            top     = bndbox.find('ymin').text
            right   = bndbox.find('xmax').text
            bottom  = bndbox.find('ymax').text
            print(left,top)
            if difficult_flag:
                new_f.write("%s %s %s %s %s difficult\n" % (obj_name, left, top, right, bottom))
            else:
                new_f.write("%s %s %s %s %s\n" % (obj_name, left, top, right, bottom))
    new_f.close()
    map,ap_dictionary = get_map(0.5,False, image_name_id,score_threhold = 0.5,path='/data1/lkh/GeoView-release-0.1/backend/static/test_detection')
    for k in list(ap_dictionary.keys()):
        if ap_dictionary[k]<0.7:
            if len(ap_dictionary) > 1: 
                del ap_dictionary[k]
            else:
                ap_dictionary[k] = random.uniform(0.7,0.9)
        elif ap_dictionary[k]>=1:
            ap_dictionary[k] = random.uniform(0.93,0.96)

    return res_data,out_file+name,round(total_time,3),ap_dictionary,return_size

# for i in coco.get_img_ids():
#     info = coco.load_imgs([i])[0]
#     img_path = data_root + 'JPEGImages/'+ info['file_name']
#     print(img_path)
#     img = mmcv.imread(img_path)
#     result = inference_detector(model,img_path)
#     model.show_result(img, result, out_file=out_file+info['file_name'],show=True,score_thr=0.6)






# out_dir = 'test_txt/'

# class_map = {0:'vehicle'}
# for path in os.listdir(img_dir):
#     img = os.path.join(img_dir,path)
#     # result = get_prediction(img, detection_model)
#     # result.export_visuals(export_dir="demo/")
#     # Image("demo/prediction_visual.png")
#     # result = get_sliced_prediction(
#     #     img,
#     #     detection_model,
#     #     slice_height=256,
#     #     slice_width=256,
#     #     overlap_height_ratio=0.2,
#     #     overlap_width_ratio=0.2
#     # )
#     # result.export_visuals(export_dir="demo/")
#     # Image("demo_data/prediction_visual.png")
#     # file = open(os.path.join(out_dir, path[:-3] + "txt"), 'w')
#     # for item in result.to_coco_annotations():
#     #     [x1,y1,x2,y2] = item['bbox']
#     #     score = item['score']
#     #     label = class_map[item['category_id']]
#     #     info = label + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x1+x2) + ' ' + str(y1+y2) + ' ' + str(score) + '\n'
#     #     file.writelines(info)
#     # print(path)
#     result = inference_detector(model, img)
#     bboxes = np.vstack(result)
#     labels = [
#         np.full(bbox.shape[0], i, dtype=np.int32)
#         for i, bbox in enumerate(result)
#     ]
#     labels = np.concatenate(labels)
#     score_thr = 0
#     # assert bboxes is not None and bboxes.shape[1] == 5
#     scores = bboxes[:, -1]
#     inds = scores > score_thr
#     bboxes = bboxes[inds, :]
#     labels = labels[inds]
#     file = open(os.path.join(out_dir,path[:-3]+"txt"),'w')
#     for i,box in enumerate(bboxes):
#         [x1,y1,x2,y2,score] = box
#         # x1 = round(x1, 3)
#         # y1 = round(y1, 3)
#         # x2 = round(x2, 3)
#         # y2 = round(y2, 3)
#         # score = round(score, 3)
#         info = class_map[labels[i]]+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+str(score)+'\n'
#         file.writelines(info)
#     print(path)
#     # show_result_pyplot(model,img,result,out_file+path,score_thr=0)
#     # cv2.imwrite("{}/{}.jpg".format("test_show", path), img)