import lib.Leap as Leap
import math
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
                self.process_gestures(controller)

                if len(hand.fingers) == 1:
                    finger = hand.fingers[0]

                    screen_to_choose = None
                    position = None
                    chosen_screen = False

                    for screen in [self.screens[0]]: # Swap new one in when you can handle multiple screens
                    #for screen in self.screens:
                        candidate = screen.intersect(finger, True)
                        
                        x_pos = candidate.x
                        y_pos = candidate.y
                        
                        # Throws out datapoints when you point off screen - have to figure out in-bounds geometry for multiscreen
                        if not (math.isnan(x_pos) or math.isnan(y_pos)):
                            screen_to_choose = screen
                            position = candidate
                            chosen_screen = True


                    if not chosen_screen: return
                    

                    x_pixels = position.x * screen_to_choose.width_pixels
                    y_pixels = screen_to_choose.height_pixels - position.y * screen_to_choose.height_pixels
                    
                    # currently only sets it in relation to the primary screen
                    self.mouse.move(x_pixels,y_pixels)                    



            """
            # Handles turning it off and on with 4 finger wave
            if len(hand.fingers) >= 4:
                result = self.timer.signal()
                if result:
                    self.on = not self.on
                    #print self.on
            """
    def process_gestures(self, controller):
        frame = controller.frame()
        hand = frame.hands[0]

        if len(hand.fingers) < 2: return

        x_pos = self.mouse.position()[0]
        y_pos = self.mouse.position()[1]
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                if len(hand.fingers) == 2:
                    self.mouse.click(x_pos, y_pos, 1)
                elif len(hand.fingers) == 3:
                    self.mouse.click(x_pos, y_pos, 2)
                break # hack so that you only count one click with multi-finger gesture

                
                
