from flask import Blueprint, request, jsonify
import os
import uuid
from applications.common.utils.http import fail_api
from applications.extensions.init_upload import photos
myfunction = Blueprint('myfunction', __name__, url_prefix='/api/myfunction')
from applications.interface.utils import get_model_info
from applications.common.utils.http import fail_api, success_api, table_api
from applications.my_interface.detection import deteciton_demo
from applications.my_interface.siamese import siamese_classification
from applications.my_interface.location import yolo_location
import random
detection_class_map = {"sum":"总数","Warship":"军舰","Ship":"民船"}
location_class_map = {"sum":"总数","radar":"雷达","runway":"跑道"}
#   检测接口
@myfunction.post('/object_detection')
def detection_api():
    print("object_detection")
    req_json = request.json
    list_data = req_json["list"]
    data = list()
    table_data = list()
    table_ap = list()
    for i,old_path in enumerate(list_data):
        res_dict,target_name,total_time,ap_dictionary,size = deteciton_demo(old_path)
        data.append({
                "id":i+1,
                "type":"目标检测",
                "before_img": old_path,
                "after_img": target_name,
            })
        for index,val in enumerate(res_dict['class']):
            table_data.append({
                "id":i+1,
                "class":detection_class_map[val],
                "bbox":res_dict['bbox'][index],
                "score":res_dict['score'][index],
                "size":res_dict['size'][index],
                'time':total_time
            })
    for k in ap_dictionary.keys():
        if k == 'sum':
            table_ap.append({
                "class":detection_class_map[k],
                "ap":round(ap_dictionary[k],3),
            })
    res = {"msg": "上传成功", "code": 0, "success": True, "data":{'imgArr':data,'tableData':table_data,'tableAP':table_ap,'size':size}}
    return jsonify(res)

@myfunction.post('/classification')
def classification_api():
    print("classification")
    req_json = request.json
    list_data = req_json["list"]
    data = list()
    table_data = list()
    return_ap = 0
    table_ap = list()
    for index in range(0,len(list_data),4):
        raw_path  = list_data[index]
        after_path_1 = list_data[index+1]
        after_path_2 = list_data[index+2]
        after_path_3 = list_data[index+3]
        predict_class_1,probability_1,total_time_1,size = siamese_classification(raw_path,after_path_1)
        predict_class_2,probability_2,total_time_2,size = siamese_classification(raw_path,after_path_2)
        predict_class_3,probability_3,total_time_3,size = siamese_classification(raw_path,after_path_3)
        if probability_1 > 0.7:
            return_ap +=1
        if probability_2 > 0.7:
            return_ap +=1
        if probability_3 > 0.7:
            return_ap +=1
        data.append({
            "id":index+1,
            "type":"孪生网络",
            "before_img": raw_path,
            "after_img_1": after_path_1,
            "after_img_2": after_path_2,
            "after_img_3": after_path_3,
        })
        table_data.append({
            "id":index+1,
            "predict_class_1":predict_class_1,
            "probability_1":probability_1,
            "time_1":total_time_1,
            "predict_class_2":predict_class_2,
            "probability_2":probability_2,
            "time_2":total_time_2,
            "predict_class_3":predict_class_3,
            "probability_3":probability_3,
            "time_3":total_time_3,
        })
        table_ap.append({
            "ap":round(return_ap/3.0,3),
        })
    res = {"msg": "上传成功", "code": 0, "success": True, "data":{'imgArr':data,'tableData':table_data,'size':size,'tableAP':table_ap}}
    return jsonify(res)

@myfunction.post('/location')
def location_api():
    print("location")
    req_json = request.json
    list_data = req_json["list"]
    data = list()
    out_data = list()
    table_data = list()
    table_ap = list()
    side_table_data = list()
    side_table_ap = list()
    for i in range(0,len(list_data),2):
        main_path  = list_data[i]
        side_path = list_data[i+1]
        main_data,side_data,[out_side_path,out_main_path],side_total_time,side_ap_dict,total_time,ap_dict,size = yolo_location(main_path,side_path)
        data.append({
                "id":i+1,
                "type":"目标定位",
                "before_img": main_path,
                "after_img": side_path
            })
        out_data.append({
                "id":i+1,
                "type":"目标定位",
                "out_main_img": out_main_path,
                "out_side_img": out_side_path
            })
        for index,val in enumerate(main_data['class']):
            table_data.append({
                "id":i+1,
                "class":location_class_map[val],
                "bbox":main_data['bbox'][index],
                "score":main_data['score'][index],
                "size":main_data['size'][index],
                "time":total_time
            })
        for index,val in enumerate(side_data['class']):
            side_table_data.append({
                "id":i+1,
                "class":location_class_map[val],
                "bbox":side_data['bbox'][index],
                "score":side_data['score'][index],
                "size":side_data['size'][index],
                "time":side_total_time
            })
        for k in ap_dict.keys():
            # ap_dict[k] = random.uniform(0.92,0.96)
            if k == 'sum':
                table_ap.append({
                    "class":location_class_map[k],
                    "ap":round(ap_dict[k],3),
                })
        for k in side_ap_dict.keys():
            # side_ap_dict[k] = random.uniform(0.80,0.87)
            if k == 'sum':
                side_table_ap.append({
                    "class":location_class_map[k],
                    "ap":round(side_ap_dict[k],3),
                })
    res = {"msg": "上传成功", "code": 0, "success": True, "data":{'imgArr':data,'outArr':out_data,'tableData':table_data,'tableAP':table_ap,'side_tableData':side_table_data,'side_tableAP':side_table_ap,'size':size}}
    return jsonify(res)


@myfunction.post('/situation')
def situation_api():
    print("situation")
    data = list()
    path = "/data1/lkh/GeoView-release-0.1/backend/static/test_situation/20090415000406.txt"
    #打开文件
    f=open(path,encoding='utf-8')
    #创建空列表
    # text=[]
    #读取全部内容 ，并以列表方式返回
    lines = f.readlines()
    i = 0      
    for line in lines:
        #去除文本中的换行等等，可以追加其他操作
        line = line.replace("\n","")
        content = line.split(',')
        data.append({
            "id":i+1,
            "jingdu":content[0],
            "weidu": content[1],
            "biaoshifu": content[4],
            "date":content[5],
            "time":content[6],
        })
        i = i + 1
    # print(data)
    res = {"msg": "上传成功", "code": 0, "success": True, "data":{'imgArr':data}}
    return jsonify(res)


