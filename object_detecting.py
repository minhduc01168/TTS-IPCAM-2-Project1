import cv2
import numpy as np
import math
from collections import defaultdict

import sys

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 1


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    #print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

def main():
    cap = cv2.VideoCapture(f'vids/{sys.argv[1]}')

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    print(frame1.shape)

    frame_count = 0

    tracker = EuclideanDistTracker()

    object_id_list = []
    dict = defaultdict(list)

    colors = []

    while cap.isOpened():
        object_count = 0
        frame_count += 1
        # print(frame_count)
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # gray = cv2.resize(gray, (1280, 720), interpolation=cv2.INTER_LINEAR)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        #erode = cv2.erode(thresh, None, iterations=3)
        dilated = cv2.dilate(thresh, None, iterations=4)
        # fgMask = cv2.Canny(dilated,20,200)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) > 500 and ((x + w//2) <= 600 and (x + w//2)>=400) and ((y + h//2)>= 125 and (y + h//2) <=350):
                #continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                object_count += 1
                
                boxes.append([x, y, w, h])
        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        cv2.putText(frame1, "Track count: {}".format(object_count), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        boxes_ids = tracker.update(boxes)

        #draw the tracking line
        for id in boxes_ids:
            dict[id[4]].append(((2*id[0]+id[2])//2, (2*id[1]+id[3])//2))

            if id[4] not in object_id_list:
                object_id_list.append(id[4])
                colors.append((np.random.randint(low=0, high=255), np.random.randint(low=0, high=255), np.random.randint(low=0, high=255)))
                start_pt = ((2*id[0]+id[2])//2, (2*id[1]+id[3])//2)
                end_pt = ((2*id[0]+id[2])//2, (2*id[1]+id[3])//2)
                cv2.line(frame1, start_pt, end_pt, colors[id[4]-1], 3)
            else:
                l = len(dict[id[4]])
                for pt in range(len(dict[id[4]])):
                    if not pt + 1 == l:
                        start_pt = (dict[id[4]][pt][0], dict[id[4]][pt][1])
                        end_pt = (dict[id[4]][pt + 1][0], dict[id[4]][pt + 1][1])
                        cv2.line(frame1, start_pt, end_pt, colors[id[4]-1], 3)

        cv2.rectangle(frame1, (400, 125), (600, 350), (0, 0, 255), 4)

        if object_count > 0:
            frame1[125:350, 400:600, (0,1)] = 0

        image = cv2.resize(frame1, (1280,720))
        #cv2.imwrite("frames/test7/frame%d.jpg" % frame_count , frame1)
        cv2.imshow("feed", image)
        #cv2.imshow("fground", dilated)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(30) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()