import cv2
import argparse

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

import utils


# Some code from https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

parser = argparse.ArgumentParser(description='Cat face parser')
parser.add_argument('--rtsp', help='RTSP video stream to camera',
                    default='')

args = parser.parse_args()

rtsp_url = args.rtsp

cap = cv2.VideoCapture(rtsp_url)

while cap.isOpened():
    ret, frame = cap.read()

    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    base_options = core.BaseOptions(
        file_name='cat.tflite', use_coral=False, num_threads=4)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    input_tensor = vision.TensorImage.create_from_array(rgbframe)

    detection_result = detector.detect(input_tensor)

    image = utils.visualize(frame, detection_result)

    cv2.imshow('frame', image)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
