import cv2
import mmcv
import numpy as np
import os
import torch
import matplotlib.pyplot as plt


def featuremap_2_heatmap(feature_map):
    assert isinstance(feature_map, torch.Tensor)
    feature_map = feature_map.detach()
    heatmap = feature_map[:,0,:,:]*0
    heatmaps = []
    for c in range(feature_map.shape[1]):
        heatmap+=feature_map[:,c,:,:]
    heatmap = heatmap.cpu().numpy()
    heatmap = np.mean(heatmap, axis=0)

    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    heatmaps.append(heatmap)

    return heatmaps

def draw_feature_map(features, save_dir = "/data1/lkh/GeoView-release-0.1/backend/static/test_detection/heatmap",heatmap_name = "heatmap",PASS_IMAGE_PATH="/data1/lkh/GeoView-release-0.1/backend/static/upload/detection/000489.bmp"):
    heatmap_str_save_path = os.path.join(save_dir,"save.txt")
    if os.path.exists(heatmap_str_save_path):
        with open(heatmap_str_save_path,"r") as f:
            names = f.readlines()
            for name in names:
                if name !="":
                    PASS_IMAGE_PATH = name
                    break
        f.close()
    index=0
    img = mmcv.imread(PASS_IMAGE_PATH)
    save_dir = "/data1/lkh/GeoView-release-0.1/backend/static/test_detection/heatmap"
    # cv2.imwrite("/data1/lkh/GeoView-release-0.1/backend/static/test_detection/heatmap/save.jpg", img)
    # img_shape = img_tensor.shape
    # img = img_tensor.mul(255).byte()
    # img = img.cpu().numpy().squeeze(0).transpose((1, 2, 0))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if isinstance(features,torch.Tensor):
        for heat_maps in features:
            heat_maps=heat_maps.unsqueeze(0)
            heatmaps = featuremap_2_heatmap(heat_maps)
            # 这里的h,w指的是你想要把特征图resize成多大的尺寸
            for heatmap in heatmaps:
                heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
                heatmap = np.uint8(255 * heatmap)
                # 下面这行将热力图转换为RGB格式 ，如果注释掉就是灰度图
                heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
                superimposed_img = img
                # plt.imshow(superimposed_img,cmap='gray')
                # plt.show()
                cv2.imwrite(os.path.join(save_dir, heatmap_name + str(index) + '.png'), img)
                index = index + 1

    else:
        for featuremap in features:
            heatmaps = featuremap_2_heatmap(featuremap)

            for heatmap in heatmaps:
                heatmap = cv2.resize(heatmap,(img.shape[1], img.shape[0]))  # 将热力图的大小调整为与原始图像相同
                heatmap = np.uint8(255 * heatmap)  # 将热力图转换为RGB格式
                heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
                superimposed_img = heatmap * 0.5 + img*0.3
                # superimposed_img = img
                # plt.imshow(superimposed_img,cmap='gray')
                # plt.show()
                # 下面这些是对特征图进行保存，使用时取消注释
                # cv2.imshow("1",superimposed_img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                cv2.imwrite(os.path.join(save_dir,heatmap_name +str(index)+'.png'), superimposed_img)
                index=index+1
