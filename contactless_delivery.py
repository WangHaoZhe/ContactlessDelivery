import package_detection
#from picamera import PiCamera
from time import sleep
import numpy as np
import os
import sys
import tarfile
import tensorflow as tf
import cv2
import time
from collections import defaultdict
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

PATH = '/home/pi/Desktop'
sleep_time = 10

sys.path.append("../..")
flag = 0

MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'

PATH_TO_CKPT = PATH+'/contactless_delivery/object_detection/models/ssd_mobilenet_v1_coco_2018_01_28/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join(PATH+'/contactless_delivery/object_detection/data', 'mscoco_label_map.pbtxt')

model_path = PATH+"/contactless_delivery/object_detection/models/ssd_mobilenet_v1_coco_2018_01_28/model.ckpt"

start = time.clock()
NUM_CLASSES = 90

end= time.clock()
print('load the model' ,(end -start))
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

person_flag = 0
def cap(name):
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        cv2.imwrite(PATH+'/contactless_delivery/'+name+'.jpg',frame)

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        writer = tf.summary.FileWriter("logs/", sess.graph)
        sess.run(tf.global_variables_initializer())
    
        loader = tf.train.import_meta_graph(model_path + '.meta')
        loader.restore(sess, model_path)
        
        cap('original')

        def detection():
            cap = cv2.imread(PATH+"/contactless_delivery/new.jpg")
            start = time.clock()
            image_np =cap

            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

            detection_info = vis_util.visualize_boxes_and_labels_on_image_array(
                image_np, np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=6)
            if detection_info[2] == 1:
                person_flag = 1
            else:
                person_flag = 0
            return person_flag
            end = time.clock()
            print('One frame detect take time:' ,end - start)
            cv2.imshow("capture", image_np)
            cv2.waitKey(1)
        
        while(1):
            cap('new')

            if package_detection.detection()>=1:
                person_info = detection()
                if person_info==0:
                    print('package delivered')
                else:
                    print('dangerous')
            else:
                print('none')
            sleep(sleep_time)


