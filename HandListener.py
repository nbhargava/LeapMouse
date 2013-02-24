import lib.Leap as Leap
import time
from pymouse import PyMouse

class Timer(object):
    def __init__(self, delay):
        self.start = time.time()
        self.delay = delay

    def signal(self):
        now = time.time()
        if now - self.start > self.delay:
            self.start = now
            return True
        else:
            return False

class HandListener(Leap.Listener):
    def __init__(self):
        super(HandListener, self).__init__()
        self.timer = Timer(2)
        self.mouse = PyMouse()

    def on_init(self, controller):
        self.on = True
        self.screens = controller.calibrated_screens

        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools))
        if not frame.hands.empty:
            hand = frame.hands[0]

            if self.on:
                if len(hand.fingers) == 1:
                    finger = hand.fingers[0]

                    screen_to_choose = self.screens[0]
                    """min_distance = screen_to_choose.distance_to_point(finger.tip_position)
                    for screen in self.screens:
                        if min_distance == -1 or screen.distance_to_point(finger.tip_position) < min_distance:
                            min_distance = screen.distance_to_point(finger.tip_position)
                            screen_to_choose = screen
                    """
                    position = screen_to_choose.intersect(finger, True)
                    
                    x_pixels = position.x * screen_to_choose.width_pixels
                    y_pixels = screen_to_choose.height_pixels - position.y * screen_to_choose.height_pixels
                    self.mouse.move(x_pixels,y_pixels)
                    #print "(%d, %d)" % (x_pixels, y_pixels)
                if len(hand.fingers) == 2:
                    x_pos = self.mouse.position()[0]
                    y_pos = self.mouse.position()[1]
                    for gesture in frame.gestures():
                        if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                            self.mouse.click(x_pos, y_pos, 1)


            """
            if len(hand.fingers) >= 4:
                result = self.timer.signal()
                if result:
                    self.on = not self.on
                    #print self.on
            """