from subprocess import Popen, PIPE
from glob import glob
import os

def start_dense():
    process_1 = Popen(["python", "superpixel.py"], stdout=PIPE)
    (output_1, err_1) = process_1.communicate()
    print(output_1)
    exit_code_1 = process_1.wait()

    process_2 = Popen(["python", "width_detection_v2.py"], stdout=PIPE)
    (output_2, err_2) = process_2.communicate()
    print(output_2)
    exit_code_2 = process_2.wait()
    stats = output_2.decode("utf-8").split("\n")

    imgs = glob(os.path.join("static", "*.jpg"))
    results = list()
    for img in imgs:
        results.append(os.path.abspath(img)) 
    
    return {"response": [{'mean':stats[-3], 'var':stats[-2]}],
        "files_info": results}