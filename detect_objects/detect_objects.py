import numpy as np
import cv2
import argparse
import math
from collections import defaultdict

def get_background(cap):
    # we will randomly select 50 frames for the calculating the median
    frame_indices = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=50) # tra ve so khung hinh trong tep video #size=50
    # we will store the frames in array
    frames = []
    for idx in frame_indices:
        # set the frame id to read that particular frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx) # chi muc cua frame
        ret, frame = cap.read() # doc tung frame
        frames.append(frame) # them frame vao list frames
    # calculate the median
    median_frame = np.median(frames, axis=0).astype(np.uint8) # tra ve gia tri trung binh va chuyen kieu du lieu
    return median_frame

# Store the center positions of the objects
center_points = {}
# Keep the count of the IDs
# each time a new object id detected, the count will increase by one
id_count = 0
line_count = 0
objects_rec_lines = [] # list chua list cac diem cua each frame
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
                # print(center_points) # in ra id: ( center_x, center_y)
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
# get the video frame height and width
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# define codec and create VideoWriter object
# create video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('D:/GITHUB/TTVNPT/TTS-IPCAM-2-Project1/detect_objects/output/output1.avi', fourcc, 5, (1280, 720))
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('D:/GITHUB/TTVNPT/TTS-IPCAM-2-Project1/detect_objects/output/output1.mp4',fourcc, 10, (frame_width, frame_height))
# fps video moi tao=10
# get the background model
background = get_background(cap)
# cv2.imshow('background', background)
# convert the background model to grayscale format
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
#cv2.imshow('background_gray', background)
frame_count = 0
consecutive_frame = 2 #số lượng khung hình liên tiếp xem xét để tính sai lệch khung hình và tính tổng (paper su dung 8)
dict = defaultdict(list)
colors = []
object_id_list = []
while (cap.isOpened()):
    ret, frame = cap.read() # kieu boolean, trả về true nếu khung có sẵn.
    if ret == True:
        frame_count += 1
        count = 0
        orig_frame = frame.copy()
        # IMPORTANT STEP: convert the frame to grayscale first
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_count % consecutive_frame == 0 or frame_count == 1: # khi o khung dau tien va so khung chia het cho consecutive_frame --> tao list luu moi
            frame_diff_list = []
        # find the difference between current frame and base frame
        frame_diff = cv2.absdiff(gray, background) # tinh toan su khac biet giua frame hien tai va nen
        # thresholding to convert the frame to binary
        ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY) # Nếu pixel<50 -->0, nếu không, else -->255.
        #cv2.imshow('image_threshold',thres)
        # remove small white noises
        img_erosion = cv2.erode(thres, np.ones((3,3), np.uint8), iterations=2)
        # dilate the frame a bit to get some more white area...
        # ... makes the detection of contours a bit easier
        dilate_frame = cv2.dilate(img_erosion, np.ones((7,7), np.uint8), iterations=2) # su dung dilating de mo rong vung trang
        #cv2.imshow('img_thres_noi', dilate_frame)
        # append the final result into the `frame_diff_list`
        frame_diff_list.append(dilate_frame)
        # if we have reached `consecutive_frame` number of frames
        if len(frame_diff_list) == consecutive_frame: # neu dat du so frame(paper=8)
            # add all the frames in the `frame_diff_list`
            sum_frames = sum(frame_diff_list)
            # find the contours around the white segmented areas
            contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # draw the contours, not strictly necessary
            for i, cnt in enumerate(contours):
                cv2.drawContours(frame, contours, i, (0, 0, 255), 3)
                #cv2.imshow('image_contour',frame)
            detections = []
            objects_rec_line = [] # list luu tru cac diem ve line cua contour in each frame

            for contour in contours:
                # continue through the loop if contour area is less than 500...
                # ... helps in removing noise detection
                if cv2.contourArea(contour) < 500:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                # get the xmin, ymin, width, and height coordinates from the contours
                if cv2.contourArea(contour) > 500 and ((x + w //2) <= 400 and (x + w //2) >= 200) and ((y + h) >= 150 and (y + h) <= 350):
                    # continue
                    count += 1
                detections.append([x, y, w, h])
                #line_x = (x + x + w) // 2
                #line_y = y + h
                #objects_rec_line.append([line_x, line_y]) # fix code o list nay
            #objects_rec_lines.append(objects_rec_line)
            #print(objects_rec_lines)
            cv2.putText(orig_frame, "Track count: {}".format(count), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)
            boxes_ids = update(detections)
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                # draw the bounding boxes
                cv2.rectangle(orig_frame, (x, y - 5), (x + w, y + h + 5), (0, 255, 0), 2)
                cv2.putText(orig_frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            for id in boxes_ids:
                dict[id[4]].append(((2 * id[0] + id[2]) // 2, (2 * id[1] + id[3]) // 2))

                if id[4] not in object_id_list:
                    object_id_list.append(id[4])
                    colors.append((np.random.randint(low=0, high=255), np.random.randint(low=0, high=255),
                                   np.random.randint(low=0, high=255)))
                    start_pt = ((2 * id[0] + id[2]) // 2, (2 * id[1] + id[3]) // 2)
                    end_pt = ((2 * id[0] + id[2]) // 2, (2 * id[1] + id[3]) // 2)
                    cv2.line(orig_frame, start_pt, end_pt, colors[id[4] - 1], 2)
                else:
                    l = len(dict[id[4]])
                    for pt in range(len(dict[id[4]])):
                        if not pt + 1 == l:
                            start_pt = (dict[id[4]][pt][0], dict[id[4]][pt][1])
                            end_pt = (dict[id[4]][pt + 1][0], dict[id[4]][pt + 1][1])
                            cv2.line(orig_frame, start_pt, end_pt, colors[id[4] - 1], 2)
            cv2.rectangle(orig_frame, (200, 150), (400, 350), (0, 255, 0), 3)
            if count > 0:
                orig_frame[150:350, 200:400, (0, 1)] = 0
            resize_orig_frame = cv2.resize(orig_frame, (1280, 720), interpolation=cv2.INTER_LINEAR)
            cv2.imshow('Detected Objects', resize_orig_frame)
            out.write(resize_orig_frame)
            #out.write(thres)
            #out.write(frame)
            #out.write(orig_frame)
            #out.write(dilate_frame)
            if cv2.waitKey(150) & 0xFF == ord('q'): # setup time video
                break
    else:
        break
cap.release() #Đóng tệp video hoặc thiết bị chụp.
cv2.destroyAllWindows()

