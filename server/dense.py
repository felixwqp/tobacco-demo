from subprocess import Popen, PIPE


def start_dense():
    process_1 = Popen(["python", "superpixel.py"], stdout=PIPE)
    (output_1, err_1) = process_1.communicate()
    print(output_1)
    exit_code_1 = process_1.wait()

    process_2 = Popen(["python", "width_detection_v2.py"], stdout=PIPE)
    (output_2, err_2) = process_2.communicate()
    print(output_2)
    exit_code_2 = process_2.wait()
    