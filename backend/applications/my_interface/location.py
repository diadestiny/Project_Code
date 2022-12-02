from PIL import Image
from applications.my_interface.location_utils.yolo import YOLO
yolo = YOLO()

main_path = '/data1/lkh/GeoView-release-0.1/backend/static/test_location/main/'
side_path = '/data1/lkh/GeoView-release-0.1/backend/static/test_location/side/'
def yolo_location(image_1,image_2):
    image = Image.open(image_1)
    side_image = Image.open(image_2)
    res_image,res_data = yolo.detect_image(image,side_image, crop = False, count=False)
    res_image2,res_data2 = yolo.detect_image(side_image,image, crop = False, count=False)
    name = image_1.split("/")[-1]
    res_image.save(main_path+name)
    res_image2.save(side_path+name)
    return res_data,res_data2,[main_path+name,side_path+name]