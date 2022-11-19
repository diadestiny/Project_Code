import mmcv
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"]  = '7'
from mmdet.datasets.api_wrappers import COCO
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import cv2
data_root = '/data1/lkh/dataset/small_ship_dataset/'
# json_file = data_root +'val.json'
out_file= '/data1/lkh/GeoView-release-0.1/backend/static/test_show/'
# coco = COCO(json_file)
config_file = '/data1/lkh/mmdet/work_dirs/detectors_cascade_rcnn_r50_1x_coco/detectors_cascade_rcnn_r50_1x_coco.py'
checkpoint_file = '/data1/lkh/mmdet/work_dirs/detectors_cascade_rcnn_r50_1x_coco/epoch_10.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')
class_map = {0:'ship'}
def deteciton_demo(img_path):
    img = mmcv.imread(img_path)
    result = inference_detector(model,img_path)
    name = img_path.split('/')[-1]
    model.show_result(img, result, out_file=out_file+name,show=True,score_thr=0.6)
    bboxes = np.vstack(result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(result)
    ]
    labels = np.concatenate(labels)
    score_thr = 0.6
    # assert bboxes is not None and bboxes.shape[1] == 5
    scores = bboxes[:, -1]
    inds = scores > score_thr
    bboxes_score = bboxes[inds, :]
    labels = labels[inds]
    res_data= dict()
    res_data['bbox'] = list()
    res_data['class'] = list()
    res_data['score'] = list()
    for i,bs in enumerate(bboxes_score):
        [x1,y1,x2,y2,score] = bs
        x1 = round(x1, 3)
        y1 = round(y1, 3)
        x2 = round(x2, 3)
        y2 = round(y2, 3)
        score = round(score, 3)
        res_data['bbox'].append([str(x1),str(y1),str(x2),str(y2)])
        res_data['class'].append(class_map[labels[i]])
        res_data['score'].append(str(score))
    return res_data,out_file+name

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