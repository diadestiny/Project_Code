from .coco import CocoDataset
from .builder import DATASETS

@DATASETS.register_module()
class SmallShip2COCODataset(CocoDataset):
    '''
    1.数据转成COCO格式，直接继承COCO （CocoDataset)）数据类，修改一下类别即可

    '''
    # CLASSES = ('airplane', 'ship', 'storage tank', 'baseball diamond', 'tennis court',
    #            'basketball court', 'ground track field', 'harbor', 'bridge', 'vehicle')

    CLASSES = ('ship',)