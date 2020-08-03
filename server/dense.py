from subprocess import Popen, PIPE
from glob import glob
import os
from superpixel import superpixel
from width_detection_v2 import width_detect
import time


def emptify_dir(dir):
    files = glob('{}/*'.format(dir))
    for f in files:
        os.remove(f)


def start_dense(filename):
    start = time.time()
    # emptify the previous results in the directory first
    emptify_dir("SegmentationData")
    emptify_dir("static")  

    superpixel(filename)

    mean, var = width_detect()
    print("Takes: {} second".format(time.time() - start))

    imgs = glob(os.path.join("static", "*.jpg"))
    results = list()
    for img in imgs:
        results.append(os.path.abspath(img)) 
    
    return {"response": [{'mean': mean, 'var': var}],
        "files_info": results}

if __name__ == "__main__":
    start_dense("target.bmp")