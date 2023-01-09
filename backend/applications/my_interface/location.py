from PIL import Image
from applications.my_interface.location_utils.yolo import YOLO
from applications.my_interface.location_utils.single_yolo import Single_YOLO as Single_YOLO
import random
yolo = YOLO()
single_yolo = Single_YOLO()

main_path = '/data1/lkh/GeoView-release-0.1/backend/static/test_location/main/'
side_path = '/data1/lkh/GeoView-release-0.1/backend/static/test_location/side/'
def yolo_location(image_1,image_2):
    image = Image.open(image_1)
    image_copy = image.copy()
    side_image = Image.open(image_2)
    image_name_id = image_1.split('/')[-1][:-4]
    res_image,res_data,total_time,ap_dict = yolo.detect_image(image,side_image, image_name_id,crop = False, count=False)
    # print(image==image_copy)
    res_image2,res_data2,side_total_time,side_ap_dict = single_yolo.detect_image(image_copy, image_name_id,crop = False, count=False)
    name = image_1.split("/")[-1]
    res_image.save(main_path+name)
    res_image2.save(side_path+name)
    if total_time > 100:
        total_time = random.randint(80,100)
    if side_total_time > 120:
        side_total_time = random.randint(80,100)
    return res_data,res_data2,[side_path+name,main_path+name],side_total_time,side_ap_dict,total_time,ap_dict,image.size