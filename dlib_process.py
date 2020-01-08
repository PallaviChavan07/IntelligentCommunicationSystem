'''
Final Project

'''

import cv2
import dlib
from enum import Enum
from time import time
import video_process


class LandMarkLoc(Enum):
    lt_eye_top_1 = 37
    lt_eye_btm_1 = 41
    lt_eye_top_2 = 38
    lt_eye_btm_2 = 40
    rt_eye_top_1 = 43
    rt_eye_btm_1 = 47
    rt_eye_top_2 = 44
    rt_eye_btm_2 = 46
    lt_eye_st_crn = 36
    lt_eye_end_crn = 39
    rt_eye_st_crn = 42
    rt_eye_end_crn = 45


LFT_EYE_TOP1 = 0
LFT_EYE_BTM1 = 1
LFT_EYE_TOP2 = 2
LFT_EYE_BTM2 = 3
RT_EYE_TOP1 = 4
RT_EYE_BTM1 = 5
RT_EYE_TOP2 = 6
RT_EYE_BTM2 = 7
LFT_EYE_ST_CNR = 8
LFT_EYE_END_CNR = 9
RT_EYE_ST_CNR = 10
RT_EYE_END_CNR = 11

EYE_STATE_INIT = -1
EYE_STATE_OPEN = 0
EYE_STATE_CLOSE = 1


class DlibProcess():
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.land_mark_predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')
        self.terminate = False
        self.frame = None
        self.face_obj = None
        self.land_mark_dict = {}
        self.window_name = 'landmark'
        self.blink_count = 0
        self.eye_state = EYE_STATE_INIT

        cv2.namedWindow(self.window_name)
        cv2.moveWindow(self.window_name, 100, 100)

    def set_image(self, image):

        self.frame = image.copy();
        # print('DlibProcess: image shape:', self.frame.shape)

    def get_faces(self):
        self.face_obj = None

        if self.frame is None:
            # print('DlibProcess(): get_faces: None objects detected')
            return False

        # convert image to gray scale
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        face_objs = self.face_detector(gray_frame, 1)
        print("DlibProcess: Number of faces detected: {}".format(len(face_objs)))
        if len(face_objs) != 1:
            # print("DlibProcess: Number of faces detected is not 1")
            return False

        self.face_obj = face_objs[0]
        return True

    def get_lanmark_data(self):
        self.land_mark_dict = {}

        if self.frame is None or self.face_obj is None:
            # print('DlibProcess(): get_lanmark_data: None objects detected')
            return False, self.blink_count

        # convert image to gray scale
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        land_mark_obj = self.land_mark_predictor(gray_frame, self.face_obj)
        # Left Eye Top 1 x, y coordinate
        self.land_mark_dict[LFT_EYE_TOP1] = (
        land_mark_obj.part(LandMarkLoc.lt_eye_top_1.value).x, land_mark_obj.part(LandMarkLoc.lt_eye_top_1.value).y)

        # Left Eye Btm 1 x, y coordinate
        self.land_mark_dict[LFT_EYE_BTM1] = (
        land_mark_obj.part(LandMarkLoc.lt_eye_btm_1.value).x, land_mark_obj.part(LandMarkLoc.lt_eye_btm_1.value).y)

        # Left Eye Top 2 x, y coordinate
        self.land_mark_dict[LFT_EYE_TOP2] = (
        land_mark_obj.part(LandMarkLoc.lt_eye_top_2.value).x, land_mark_obj.part(LandMarkLoc.lt_eye_top_2.value).y)
        # Left Eye Btm 2 x, y coordinate
        self.land_mark_dict[LFT_EYE_BTM2] = (
        land_mark_obj.part(LandMarkLoc.lt_eye_btm_2.value).x, land_mark_obj.part(LandMarkLoc.lt_eye_btm_2.value).y)

        # Right Eye Top 1 x, y coordinate
        self.land_mark_dict[RT_EYE_TOP1] = (
        land_mark_obj.part(LandMarkLoc.rt_eye_top_1.value).x, land_mark_obj.part(LandMarkLoc.rt_eye_top_1.value).y)
        # Right Eye Btm 1 x, y coordinate
        self.land_mark_dict[RT_EYE_BTM1] = (
        land_mark_obj.part(LandMarkLoc.rt_eye_btm_1.value).x, land_mark_obj.part(LandMarkLoc.rt_eye_btm_1.value).y)

        # Right Eye Top 2 x, y coordinate
        self.land_mark_dict[RT_EYE_TOP2] = (
        land_mark_obj.part(LandMarkLoc.rt_eye_top_2.value).x, land_mark_obj.part(LandMarkLoc.rt_eye_top_2.value).y)
        # Right Eye Btm 2 x, y coordinate
        self.land_mark_dict[RT_EYE_BTM2] = (
        land_mark_obj.part(LandMarkLoc.rt_eye_btm_2.value).x, land_mark_obj.part(LandMarkLoc.rt_eye_btm_2.value).y)

        # Left Eye start corner x, y coordinate
        self.land_mark_dict[LFT_EYE_ST_CNR] = (
        land_mark_obj.part(LandMarkLoc.lt_eye_st_crn.value).x, land_mark_obj.part(LandMarkLoc.lt_eye_st_crn.value).y)

        # Left Eye end corner x, y coordinate
        self.land_mark_dict[LFT_EYE_END_CNR] = (
        land_mark_obj.part(LandMarkLoc.lt_eye_end_crn.value).x, land_mark_obj.part(LandMarkLoc.lt_eye_end_crn.value).y)

        # Right Eye start corner x, y coordinate
        self.land_mark_dict[RT_EYE_ST_CNR] = (
        land_mark_obj.part(LandMarkLoc.rt_eye_st_crn.value).x, land_mark_obj.part(LandMarkLoc.rt_eye_st_crn.value).y)

        # Right Eye end corner x, y coordinate
        self.land_mark_dict[RT_EYE_END_CNR] = (
        land_mark_obj.part(LandMarkLoc.rt_eye_end_crn.value).x, land_mark_obj.part(LandMarkLoc.rt_eye_end_crn.value).y)

        lt_h1 = land_mark_obj.part(LandMarkLoc.lt_eye_btm_1.value).y - land_mark_obj.part(
            LandMarkLoc.lt_eye_top_1.value).y
        lt_h2 = land_mark_obj.part(LandMarkLoc.lt_eye_btm_2.value).y - land_mark_obj.part(
            LandMarkLoc.lt_eye_top_2.value).y
        lt_width = self.land_mark_dict[LFT_EYE_END_CNR][0] - self.land_mark_dict[LFT_EYE_ST_CNR][0]
        lt_h1_ratio = lt_h1 / lt_width
        lt_h2_ratio = lt_h2 / lt_width

        # EYE_STATE_OPEN self.total_blink_count, self.eye_state

        eye_status = 'OPEN'
        if lt_h1_ratio <= 0.18:
            eye_status = 'CLOSE'
            if self.eye_state == EYE_STATE_OPEN:
                self.eye_state = EYE_STATE_CLOSE
                self.blink_count += 1
        else:
            if self.eye_state == EYE_STATE_INIT or self.eye_state == EYE_STATE_CLOSE:
                self.eye_state = EYE_STATE_OPEN

        print('LT1: ', lt_h1, 'LT2: ', lt_h2, 'lt_h1_ratio: ', lt_h1_ratio, 'lt_h2_ratio: ', lt_h2_ratio,
              'EYE sttus', eye_status, 'blink_count: ', self.blink_count)

        return True, self.blink_count

    def show_image(self):

        disp_img = self.frame.copy()

        if len(self.land_mark_dict) == 0:
            disp_img = cv2.line(disp_img, (disp_img.shape[1] - 50, int(disp_img.shape[0] / 2)),
                                (disp_img.shape[1] - 50, int(disp_img.shape[0] / 2)), (0, 0, 255), 40)
        else:
            disp_img = cv2.line(disp_img, (disp_img.shape[1] - 50, int(disp_img.shape[0] / 2)),
                                (disp_img.shape[1] - 50, int(disp_img.shape[0] / 2)), (0, 255, 0), 40)

        cv2.putText(disp_img, "Blink Count {}".format(self.blink_count), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (255, 0, 0), 1, cv2.LINE_AA)

        for key, val in self.land_mark_dict.items():
            # value contains x,y coordinate points
            disp_img = cv2.line(disp_img, (int(val[0]), int(val[1])), (int(val[0]), int(val[1])), (0, 0, 255), 2)
        # print('disp_img,shape', disp_img.shape)
        disp_img = cv2.resize(disp_img, (int(disp_img.shape[0] * 0.75), int(disp_img.shape[1] * 0.75)))

        # Display the resulting frame
        cv2.imshow(self.window_name, disp_img)
        key = cv2.waitKey(1)
        if key == ord('e'):
            self.terminate = True

    def start_process(self, display_image):

        # create an object of Video Process
        vid_process = video_process.VideoProcess()

        status = vid_process.start_capture()
        if status == False:
            print('Error: DlibProcess: Failed to open camera')
            self.terminate = True

        while self.terminate == False:
            self.land_mark_dict = {}
            self.frame = None

            # Capture frame-by-frame
            status, frame = vid_process.get_frame()
            if not status:
                print('Error: DlibProcess: Failed to capture image')
                self.terminate = True
            else:
                # set the captured image for processing
                self.set_image(frame)

                # Got frame from camera. Get get_faces
                if self.get_faces() == True:
                    self.get_lanmark_data()

                self.show_image()

        vid_process.terminate_process()

    def get_blinkcount(self, duration=3):

        self.blink_count = 0

        # create an object of Video Process
        vid_process = video_process.VideoProcess()

        status = vid_process.start_capture()
        if not status:
            print('Error: DlibProcess: get_blinkcount: Failed to open camera')
            return status, self.blink_count

        start_time = time()
        while time() - start_time <= 1.0 * duration:
            self.land_mark_dict = {}
            self.frame = None

            # Capture frame-by-frame
            status, frame = vid_process.get_frame()
            if not status:
                print('Error: DlibProcess:get_blinkcount: Failed to capture image')
                self.blink_count = 0
                return status, self.blink_count
            else:
                # set the captured image for processing
                self.set_image(frame)

                # Got frame from camera. Get get_faces
                if self.get_faces() == True:
                    status = self.get_lanmark_data()

                self.show_image()

        vid_process.terminate_process()

        return True, self.blink_count

