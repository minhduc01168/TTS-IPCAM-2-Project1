import numpy as np
import cv2
import argparse

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


cap = cv2.VideoCapture('D:/GITHUB/TTVNPT/TTS-IPCAM-2-Project1/detect_objects/input/video.avi')
# get the video frame height and width
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# define codec and create VideoWriter object
# create video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('D:/GITHUB/TTVNPT/TTS-IPCAM-2-Project1/detect_objects/output/output1.avi', fourcc, 10, (1280, 720))
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
while (cap.isOpened()):
    ret, frame = cap.read() # kieu boolean, trả về true nếu khung có sẵn.
    if ret == True:
        frame_count += 1
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
            for contour in contours:
                # continue through the loop if contour area is less than 500...
                # ... helps in removing noise detection
                if cv2.contourArea(contour) < 500:
                    continue
                # get the xmin, ymin, width, and height coordinates from the contours
                (x, y, w, h) = cv2.boundingRect(contour)
                # draw the bounding boxes
                cv2.rectangle(orig_frame, (x, y - 5), (x + w, y + h + 5), (0, 255, 0), 2)
            resize_orig_frame = cv2.resize(orig_frame, (1280, 720), interpolation=cv2.INTER_LINEAR)
            cv2.imshow('Detected Objects', resize_orig_frame)
            out.write(resize_orig_frame)
            #out.write(thres)
            #out.write(frame)
            #out.write(orig_frame)
            #out.write(dilate_frame)
            if cv2.waitKey(200) & 0xFF == ord('q'): # setup time video
                break
    else:
        break
cap.release() #Đóng tệp video hoặc thiết bị chụp.
cv2.destroyAllWindows()

