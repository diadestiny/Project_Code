from flask import Blueprint, request, jsonify
from flask import current_app
import os
import time
# from applications.common.utils import upload as type_utils,upload_curd
from applications.common.utils.http import fail_api
from applications.extensions.init_upload import photos
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
    return fail_api()
