import numpy as np
from PIL import Image
import os
from siamese import Siamese

if __name__ == "__main__":
    model = Siamese()
    for path in os.listdir("datasets/boat/easy/"):
        image_1 = os.path.join("datasets/boat/easy/",path)
        image_1 = Image.open(image_1)
        image_2 = os.path.join("datasets/boat/mid/",path)
        image_2 = Image.open(image_2)
        predict_class,probability = model.detect_image(image_1, image_2)
        print(predict_class,probability)

    # image_2 = "datasets/boat/images/boat1.png"



