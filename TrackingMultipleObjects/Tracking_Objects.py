import cv2
import numpy as np
import argparse
import math

# Store the center positions of the objects
center_points = {}
# Keep the count of the IDs
# each time a new object id detected, the count will increase by one
id_count = 0

def update(objects_rect):# objects_rect tọa độ xmin,ymin, w,h
    # Objects boxes and ids
    objects_bbs_ids = []
    # Get center point of new object
    for rect in objects_rect:
        x, y, w, h = rect
        cx = (x + x + w) // 2 # cx cua toa do tam bounding
        cy = (y + y + h) // 2 # cy cua toa do tam bounding

        # Find out if that object was detected already
        same_object_detected = False
        global center_points, id_count # global thay doi bien toan cuc
        for id, pt in center_points.items(): # lay cap id tọa độ
            dist = math.hypot(cx - pt[0], cy - pt[1])  # tra ve sqrt(x*x + y*y).

            if dist < 45:
                center_points[id] = (cx, cy)
                print(center_points) # in ra id: ( center_x, center_y)
                objects_bbs_ids.append([x, y, w, h, id])
                same_object_detected = True
                break

        # New object is detected we assign the ID to that object
        if same_object_detected is False:
            center_points[id_count] = (cx, cy)
            objects_bbs_ids.append([x, y, w, h, id_count])
            id_count += 1

    # Clean the dictionary by center points to remove IDS not used anymore
    new_center_points = {}
    for obj_bb_id in objects_bbs_ids:
        _, _, _, _, object_id = obj_bb_id
        center = center_points[object_id]
        new_center_points[object_id] = center
    # Update dictionary with IDs not used removed
    center_points = new_center_points.copy()
    return objects_bbs_ids

cap = cv2.VideoCapture('D:/GITHUB/TTVNPT/TTS-IPCAM-2-Project1/detect_objects/input/video.avi')
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # ret, frame = cap.read()
    diff = cv2.absdiff(frame1, frame2)  # this method is used to find the difference bw two  frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #cv2.imshow('gray',blur)
    # here i would add the region of interest to count the single lane cars
    height, width = blur.shape
    print(height, width)

    # thresh_value = cv2.getTrackbarPos('thresh', 'trackbar')
    _, threshold = cv2.threshold(blur, 23, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, (1, 1), iterations=1)
    contours, _, = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    # DRAWING RECTANGLE BOXED
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 500:
            continue
        detections.append([x, y, w, h])

        #cv2.rectangle(frame1, (x,y),(x+w, y+h), (0,255,0), 2)
        #cv2.putText(frame1, 'status: movement',(10,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    # cv2.drawContours(frame1,contours, -1, (0,255,0), 2)
    # cv2.imshow('frame',frame1)
    # object tracking
    boxes_ids = update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(frame1, str(id), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('frame', frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    # cv2.imshow('inter',dilated)
    # cv2.imshow('blur', blur)
    # cv2.imshow('threshold', threshold)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
cv2.destroyAllWindows()