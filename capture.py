import cv2 as cv
import gui


class FrameProcessor:
    def __init__(self, frame):
        self.frame = frame

    def draw_piano(self):
        # TODO: draw piano
        # draw piano on self.image
        self.frame = self.frame

    def process(self):
        if self.frame is not None:
            # do image process stuffs here
            self.frame = cv.flip(self.frame, 1)
            # draw_piano()
            self.frame = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)


class VideoStream:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    """
        Returns raw image directly from the camera without processing
    """
    def get_next_frame_raw(self):
        ret, frame = self.cap.read()
        return frame

    """
        Returns an Image Frame processed by Frame Processor
    """
    def get_next_frame(self):
        frame = self.get_next_frame_raw()

        frame_processor = FrameProcessor(frame)
        frame_processor.process()

        frame = frame_processor.frame
        return frame

    def destroy(self):
        self.cap.release()
        gui.DEBUG_LOG("Capture Device Released")

