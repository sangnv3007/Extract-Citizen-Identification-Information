import cv2
import numpy as np
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import os
import re
import base64
import json
# Funtions
# Ham decode, endecode


def EncodeImage(pathImageEncode):
    with open(pathImageEncode, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message


def EndecodeImage(base64_img):
    base64_img_bytes = base64_img.encode('utf-8')
    with open('decoded_image.png', 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)
# Ham get output_layer


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1]
                     for i in net.getUnconnectedOutLayers()]
    return output_layers

# Ham ve cac boxes len anh


def draw_prediction(img, classes, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes)
    color = (0, 0, 255)
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

# Transform sang toa do dich


def perspective_transoform(image, points):
    # Use L2 norm
    width_AD = np.sqrt(
        ((points[0][0] - points[3][0]) ** 2) + ((points[0][1] - points[3][1]) ** 2))
    width_BC = np.sqrt(
        ((points[1][0] - points[2][0]) ** 2) + ((points[1][1] - points[2][1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))  # Get maxWidth
    height_AB = np.sqrt(
        ((points[0][0] - points[1][0]) ** 2) + ((points[0][1] - points[1][1]) ** 2))
    height_CD = np.sqrt(
        ((points[2][0] - points[3][0]) ** 2) + ((points[2][1] - points[3][1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))  # Get maxHeight

    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])
    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(points, output_pts)
    out = cv2.warpPerspective(
        image, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    return out

# Ham check classes


def check_enough_labels(labels, classes):
    for i in classes:
        bool = i in labels
        if bool == False:
            return (False)
    return (True)
# Ham load model Yolo


def load_model(path_weights_yolo, path_clf_yolo, path_to_class):
    weights_yolo = path_weights_yolo
    clf_yolo = path_clf_yolo
    net = cv2.dnn.readNet(weights_yolo, clf_yolo)
    with open(path_to_class, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes

# Ham getIndices


def getIndices(image, net, classes):
    # image = cv2.imread(path_to_image)
    # net = load_model('model/rec/yolov4-custom_rec.weights','model/rec/yolov4-custom_rec.cfg')
    (Width, Height) = (image.shape[1], image.shape[0])
    boxes = []
    class_ids = []
    confidences = []
    conf_threshold = 0.6
    nms_threshold = 0.4
    scale = 0.00392
    # (416,416) img target size, swapRB=True,  # BGR -> RGB, center crop = False
    blob = cv2.dnn.blobFromImage(
        image, scale, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, conf_threshold, nms_threshold)
    return indices, boxes, classes, class_ids, image, confidences
# Ham load model vietOCr recognition


def vietocr_load():
    config = Cfg.load_config_from_name('vgg_transformer')
    config['weights'] = './model/transformerocr.pth'
    config['cnn']['pretrained'] = False
    config['device'] = 'cpu'
    config['predictor']['beamsearch'] = False
    detector = Predictor(config)
    return detector

# Ham crop image tu 4 goc cua CCCD


def ReturnCrop(pathImage):
    image = cv2.imread(pathImage)
    indices, boxes, classes, class_ids, image, confidences = getIndices(image, net_det, classes_det)
    list_boxes = []
    label = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        # print(box,str(classes[class_ids[i]]))
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        list_boxes.append([x+w/2, y+h/2])
        label.append(str(classes[class_ids[i]]))
    label_boxes = dict(zip(label, list_boxes))
    if (check_enough_labels(label_boxes, classes)):
        source_points = np.float32([label_boxes['top_left'], label_boxes['bottom_left'],
                                    label_boxes['bottom_right'], label_boxes['top_right']])
        crop = perspective_transoform(image, source_points)
        return crop
    # else:
    #     print("Error ! Citizen Identification not found.")
    #     #obj = MessageInfo(None,"Failed", "Error ! Citizen Identification not found.")
# Ham tra ve ket qua thong tin CCCD
# Upload part


def ReturnInfoCard(pathImage):
    crop = ReturnCrop(pathImage)
    # Trich xuat thong tin tu imageCrop
    if (crop is not None):
        indices, boxes, classes, class_ids, image, confidences = getIndices(crop, net_rec, classes_rec )
        dict_home, dict_address, dict_features = {}, {}, {}
        home_text, address_text, features_text = [], [], []
        label_boxes = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            label_boxes.append(str(classes[class_ids[i]]))
            # draw_prediction(crop, classes[class_ids[i]], confidences[i], round(x), round(y), round(x + w), round(y + h))
            imageCrop = image[round(y): round(y + h), round(x):round(x + w)]
            img = Image.fromarray(imageCrop)
            s = detector.predict(img)
            if (class_ids[i] == 0):
                id_card = s
            if (class_ids[i] == 1):
                name_card = s
            if (class_ids[i] == 2):
                dob_card = s
            if (class_ids[i] == 3):
                sex_card = s
            if (class_ids[i] == 4):
                nationality_card = s
            if (class_ids[i] == 5):
                dict_home.update({s: y})
            if (class_ids[i] == 6):
                dict_address.update({s: y})
            if (class_ids[i] == 7):
                doe_card = s
            if (class_ids[i] == 8):
                dict_features.update({s: y})
            if (class_ids[i] == 9):
                issue_date_card = s
        classesFront = ['id', 'name', 'dob', 'sex',
                        'nationality', 'home', 'address', 'doe', 'image']
        classesBack = ['features', 'issue_date']
        if (check_enough_labels(label_boxes, classesBack)):
            type = "cccd_back"
            status_text = "Successful"
            message_text = "Thành công"
            for i in sorted(dict_features.items(),
                            key=lambda item: item[1]): features_text.append(i[0])
            features_text = " ".join(features_text)
            obj = ExtractCardBack(
                features_text, issue_date_card, type, status_text, message_text)
            return obj
        if (check_enough_labels(label_boxes, classesFront)):
            type = "cccd_front"
            status_text = "Successful"
            message_text = "Thành công"
            for i in sorted(dict_home.items(),
                            key=lambda item: item[1]): home_text.append(i[0])
            for i in sorted(dict_address.items(),
                            key=lambda item: item[1]): address_text.append(i[0])
            home_text = " ".join(home_text)
            address_text = " ".join(address_text)
            obj = ExtractCardFront(id_card, name_card, dob_card, sex_card, nationality_card, home_text,
                                   address_text, doe_card, type, status_text, message_text)
            return obj
    else:
        obj = MessageInfo(None, "Failed", "Error! Try another image again !")
        return obj
detector = vietocr_load()
net_det, classes_det = load_model('./model/det/yolov4-tiny-custom_det.weights', './model/det/yolov4-tiny-custom_det.cfg', './model/det/obj_det.names')
net_rec, classes_rec= load_model('./model/rec/yolov4-custom_rec.weights', './model/rec/yolov4-custom_rec.cfg', './model/rec/obj_rec.names')
# Class object
class ExtractCardFront:
    def __init__(self, id, name, dob, sex, nationality, home, address, doe, type, status, message):
        self.id = id
        self.name = name
        self.dob = dob
        self.sex = sex
        self.nationality = nationality
        self.home = home
        self.address = address
        self.doe = doe
        self.type = type
        self.status = status
        self.message = message


class ExtractCardBack:
    def __init__(self, features, issue_date, type, status, message):
        self.features = features
        self.issue_date = issue_date
        self.type = type
        self.status = status
        self.message = message


class MessageInfo:
    def __init__(self, type, status, message):
        self.type = type
        self.status = status
        self.message = message
