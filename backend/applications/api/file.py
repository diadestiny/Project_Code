from flask import Blueprint, request, jsonify
from flask import current_app
import os
import time
import pandas as pd

# from applications.common.utils import upload as type_utils,upload_curd
from applications.common.utils.http import fail_api
from applications.extensions.init_upload import photos
from matplotlib.font_manager import FontProperties
file_api = Blueprint('file_api', __name__, url_prefix='/api/file')
num_photo = 0
#   上传接口
@file_api.post('/upload')
def upload_api():
    print("upload")
    if 'files' in request.files:
        type_ = request.form['type']
        photos_ = request.files.getlist("files")
        mime = request.files['files'].content_type
        data = list()
        if type_ == "目标检测":
            for photo in photos_:
                if photo.filename[0]=="_":
                    photo.filename =  photo.filename[1:]
                photos.save(photo, folder = 'detection',name=photo.filename[:-4] + ".")
                file_url = '/data1/lkh/GeoView-release-0.1/backend/static/upload/detection/'+ photo.filename
                data.append({
                    "src": file_url,
                    "filename": photo.filename,
                })
            res = {"msg": "上传成功", "code": 0, "success": True, "data": data}
            return jsonify(res)
        elif type_ == "孪生分类":
            if len(photos_) == 1:
                    photos_[0].filename = photos_[0].filename.replace("_","")
                    file_url1 = '/data1/lkh/Siamese-pytorch/datasets/warships/images/'+ photos_[0].filename
                    file_url2 = '/data1/lkh/Siamese-pytorch/datasets/warships/easy/' + photos_[0].filename
                    file_url3 = '/data1/lkh/Siamese-pytorch/datasets/warships/mid/'+ photos_[0].filename
                    file_url4 = '/data1/lkh/Siamese-pytorch/datasets/warships/hard/' + photos_[0].filename
                    data.append({
                        "src": file_url1,
                        "filename": photos_[0].filename,
                    })
                    data.append({
                        "src": file_url2,
                        "filename":  photos_[0].filename,
                    })
                    data.append({
                        "src": file_url3,
                        "filename": photos_[0].filename,
                    })
                    data.append({
                        "src": file_url4,
                        "filename":  photos_[0].filename,
                    })
            else:
                for i in range(0,len(photos_),2):
                    # timestamp = str(time.time()).split(".")[0]
                    photos_[i].filename = photos_[i].filename.replace("_","")
                    photos_[i+1].filename = photos_[i+1].filename.replace("_","")
                    file_url1 = '/data1/lkh/GeoView-release-0.1/backend/static/upload/classification_before/'+ photos_[i].filename
                    file_url2 = '/data1/lkh/GeoView-release-0.1/backend/static/upload/classification_after/'+ photos_[i+1].filename
                    if os.path.exists(file_url1):
                        os.remove(file_url1)
                    if os.path.exists(file_url2):
                        os.remove(file_url2)
                    photos.save(photos_[i], folder = 'classification_before',name=photos_[i].filename[:-4]+ ".")
                    photos.save(photos_[i+1], folder = 'classification_after',name=photos_[i+1].filename[:-4]+ ".")
                    
                    data.append({
                        "src": file_url1,
                        "filename": photos_[i].filename,
                    })
                    data.append({
                        "src": file_url2,
                        "filename":  photos_[i+1].filename,
                    })
            res = {"msg": "上传成功", "code": 0, "success": True, "data": data}
            return jsonify(res)
        elif type_ == '目标定位':
            for i in range(0,len(photos_),2):
                photos_[i].filename = photos_[i].filename.replace("_","")
                photos_[i+1].filename = photos_[i+1].filename.replace("_","")
                file_url1 = '/data1/lkh/GeoView-release-0.1/backend/static/upload/location_main/'+ photos_[i].filename
                file_url2 = '/data1/lkh/GeoView-release-0.1/backend/static/upload/location_side/'+ photos_[i+1].filename
                if os.path.exists(file_url1):
                    os.remove(file_url1)
                if os.path.exists(file_url2):
                    os.remove(file_url2)
                photos.save(photos_[i], folder = 'location_main',name=photos_[i].filename[:-4] + ".")
                photos.save(photos_[i+1], folder = 'location_side',name=photos_[i+1].filename[:-4] + ".")
                
                data.append({
                    "src": file_url1,
                    "filename": photos_[i].filename,
                })
                data.append({
                    "src": file_url2,
                    "filename":  photos_[i+1].filename,
                })
            res = {"msg": "上传成功", "code": 0, "success": True, "data": data}
            return jsonify(res)
        elif type_ == '态势推理':
            import matplotlib.pyplot as plt
            path = '/data1/lkh/GeoView-release-0.1/backend/static/test_situation/'+photos_[0].filename
            photos_[0].save(path)
            f=open(path,encoding='utf-8')
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
            plt_data = pd.read_csv(path, sep=',').iloc[:, 0:2].values
            # 画样本数据库
            # font = FontProperties(fname="/data1/lkh/GeoView-release-0.1/backend/static/test_situation/SIMKAI.TTF", size=14)
            plt.figure(figsize=(10, 8),dpi=200)
            # plt.rcParams['font.sans-serif'] = ['STIXNonUnicode']  # 用来正常显示中文标签
            plt.scatter(plt_data[:, 1], plt_data[:, 0], c='r', marker='o', label='real data')
            # plt.xlabel('纬度', fontproperties=font)
            # plt.ylabel('经度', fontproperties=font)
            plt.legend(loc='upper left')
            plt.grid()
            plt.savefig(path.replace('txt','png'), dpi=200, bbox_inches='tight')
            plt.clf()
            # plt.close()
            print(path)
            res = {"msg": "上传成功", "code": 0, "success": True, "data":data}
    return jsonify(res)

    return fail_api()
