from PIL import Image, ImageGrab
import cv2 as cv
import numpy as np

def show_image(img):
    """ Muestra una imagen en jupyter notebook sin que se crashee la ventana """
    cv.imshow('',img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def cv2PIL(img):
    """ Convierte una imagen de opencv a Pillow """
    return Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))

def PIL2cv(img):
    return np.array(img.convert('RGB'))[:, :, ::-1].copy()

def delete_multiple_element(list_object, indices):
    indices = sorted(indices, reverse=True)
    for idx in indices:
        if idx < len(list_object):
            list_object.pop(idx)