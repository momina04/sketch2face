# Adapted from https://medium.freecodecamp.org/sketchify-turn-any-image-into-a-pencil-sketch-with-10-lines-of-code-cf67fa4f68ce
"""
Programmatic image-to-sketch recoloring

Usage:
    sketchify.py [options]
                 
Options:
    -h --help                               show this screen.
    --images_path=<string>                  path to source images 
    --output_path=<string>                  output path to save sketchified versions                  
                        
"""
import numpy as np
from docopt import docopt
from PIL import Image
import os
import scipy.ndimage
import matplotlib.pyplot as plt


def sketchify(img):
    img_array = np.asarray(img)
    gray_img = grayscale(img_array)
    inverted_img = 255-gray_img
    blur_img = scipy.ndimage.filters.gaussian_filter(inverted_img, sigma=10)
    dodged_img = dodge(blur_img, gray_img)
    final_img_array = sharpen_contrast(dodged_img).astype('uint8')
    final_img = Image.fromarray(final_img_array, 'L')
    return final_img

def sharpen_contrast(img):
    maxval = img.max()
    minval = img.min()
    range = maxval - minval
    contrasted = (img - minval) * 255/range
    contrasted[contrasted > 255] = 255 # just in case
    return contrasted


def grayscale(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def dodge(front, back):
    result = front * 255 / (255-back)
    result[back==255] = 255
    result[result>255] = 255
    return result

def sketchify_images(src_dir, target_dir):
    for root, _, fnames in sorted(os.walk(src_dir)):
        for fname in fnames:
            if fname == '.DS_Store':
                continue
            img = Image.open(os.path.join(root, fname)).convert('RGB')
            sketch = sketchify(img)
            sketch.save(os.path.join(target_dir, fname))


if __name__ == "__main__":
    np.seterr(divide='ignore')
    args = docopt(__doc__)
    images_path = args['--images_path']
    output_path = args['--output_path']
    sketchify_images(images_path, output_path)
    





