import cv2
import numpy as np
from PIL import Image as PilImage
from enum import Enum
class ImageTypeEnum(Enum):
    PILLOW = "PILLOW"
    CV2 = "CV2"


def openCVimageToPillowImage(openCVimage) -> PilImage:
    # You may need to convert the color.
    img = cv2.cvtColor(openCVimage, cv2.COLOR_BGR2RGB)
    return PilImage.fromarray(img)