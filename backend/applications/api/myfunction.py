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

#   检测接口
@myfunction.post('/object_detection')
def detection_api():
    print("object_detection")
    req_json = request.json
    list_data = req_json["list"]
    data = list()
    table_data = list()
    for i,old_path in enumerate(list_data):
        res_dict,target_name = deteciton_demo(old_path)
        data.append({
                "id":i+1,
                "type":"目标检测",
                "before_img": old_path,
                "after_img": target_name,
            })
        for index,val in enumerate(res_dict['class']):
            table_data.append({
                "id":i+1,
                "class":val,
                "bbox":res_dict['bbox'][index],
                "score":res_dict['score'][index]
            })
        # print(table_data)
    res = {"msg": "上传成功", "code": 0, "success": True, "data":{'imgArr':data,'tableData':table_data}}
    return jsonify(res)

@myfunction.post('/classification')
def clssification_api():
    print("classification")
    req_json = request.json
    list_data = req_json["list"]
    data = list()
    table_data = list()
    for index in range(0,len(list_data),2):
        raw_path  = list_data[index]
        after_path = list_data[index+1]
        predict_class,probability = siamese_classification(raw_path,after_path)
        data.append({
                "id":index+1,
                "type":"目标检测",
                "before_img": raw_path,
                "after_img": after_path
            })
        table_data.append({
            "id":index+1,
            "predict_class":predict_class,
            "probability":probability,
        })
        # print(table_data)
    res = {"msg": "上传成功", "code": 0, "success": True, "data":{'imgArr':data,'tableData':table_data}}
    return jsonify(res)




