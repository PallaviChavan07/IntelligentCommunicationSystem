'''
Final Project

'''

import cv2


class VideoProcess():
    def __init__(self):
        self.camera_dev = None
        self.frame = None
        self.window_name = 'source'
        self.terminate = False

    def start_capture(self):
        self.camera_dev = cv2.VideoCapture(1)
        if not self.camera_dev.isOpened():
            print('Error: Failed to open Camera')
            self.camera_dev = None
            return False
        # height = self.camera_dev.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        # width = self.camera_dev.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # print('VideoProcess: start_capture: height = ', height, 'width', width)

        return True

    def get_frame(self):

        self.fame = None

        # Capture frame-by-frame
        status, frame = self.camera_dev.read()
        if not status:
            print('Error: Failed to capture image')
            return False, self.fame

        # is it necessary to flip?
        # gray_frame = cv2.flip(gray_frame, 1)
        self.fame = frame.copy()
        return True, self.fame

    def start_process(self, display_image):
        status = self.start_capture()
        if status == False:
            print('Error: Failed to open camera')
            self.terminate = True

        while self.terminate == False:

            # Capture frame-by-frame
            status, frame = self.get_frame()
            if not status:
                print('Error: Failed to capture image')
                self.terminate = True
            else:
                if display_image == True:
                    self.show_image()

        self.terminate_process()

    def show_image(self):
        # Display the resulting frame
        cv2.imshow(self.window_name, self.frame)
        key = cv2.waitKey(1)
        if key == ord('e'):
            self.terminate = True

    def terminate_process(self):
        # release the capture
        self.camera_dev.release()
        cv2.destroyAllWindows()
