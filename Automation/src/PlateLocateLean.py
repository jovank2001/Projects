'''
Class for Kaiser Plate detection
Optimized for live detection
Written by Jovan Koledin
'''

import cv2
from PIL import Image
import numpy as np
from moviepy.editor import VideoFileClip

class PlateLocate:
    #General class constants
    #Initially calibrated for use with Hotline shear layoff crane and camera 118 for alumium plates
    #All values in pixel coord unless specified
    PIXEL_THRESH = 0 #Represents PIXEL_THRESH specified in runfile
    PLATE_START_BOUND = 400 #Lowest point in which a leading edge poll can start detecting
    THRESH = 70 #Pixel magnitude for image thresholding 
    BACKGROUND_PATH = "" #Set in PlateLocateTest
    BACKGROUND_IMAGE = [] 
    FRAMES_THRESH_CROSSED_BUFFER = 2 #Number of frames with which leading edge must cross threshold consecutively before width detection
    LARGEST_PLATE = 100 #Inches
    SMALLEST_PLATE = 40 #Inches
    #Constants that determine where we look for our width points, all values are in pixels (bounding box)
    #These will be camera specific and are currently calibrated for videos of 1920X1280 resolution 
    #Can be found using pixspy.com for other cameras
    BOTTOM_RIGHT_LEFT_BOUND = 800
    BOTTOM_RIGHT_RIGHT_BOUND = 1350
    BOTTOM_LEFT_LEFT_BOUND = 400
    LOWER_BOUND = 1070
    ROLLER_CENTER = [894, 855] #Center of the Roller
    VERTICAL_TRAVEL = 25 #How far the bottom left corner y-pixel can deviate from the bottom right corner y-pixel

    #Globals that are changing, dont change these values
    width_subtract_image = []
    previous_lowest_point = 0
    width_set = False
    thresh_crossed = False
    frames_thresh_crossed = 0
    plate_moving_down_frames = 0
    previous_width = 0
    previous_frame = []
    good_set_point_left = [0, 0]
    good_set_point_right = [0, 0]
    bottom_left = [10000, 0]
    moved_down_flag = False
    bottom_right = [0, 0]
    width_final = 0
    center_dist = 0
    width_frames = 0
    plate_moved_frames = 0
    plate_picked_up = False

    def __init__(self, pixel_thresh, background_path):
        '''
        Establish initial parameters
        @params 
            pixel_thresh: Pixel point where rollers are desired to stop rolling.
                          Also point used to start looking for plate width points.
            background_path: Path to image which best represents what camera sees when there is no plate present.
        '''
        self.PIXEL_THRESH = pixel_thresh
        self.BACKGROUND_PATH = background_path
        self.BACKGROUND_IMAGE = cv2.imread(background_path)
        self.previous_frame = cv2.imread(background_path)

    def activateStop(self):
        '''
        Signifies that plate has crossed threshold
        '''
        self.thresh_crossed = True
        self.plate_moving_down_frames = 0
        self.moved_down_flag = False
        print("\nPlate crossed threshold")   

    def convertPixelWidthToInches(self, pixelWidth, yPixel):
        '''
        Convert pixel width to inches using simple linear equation 
        Can be improved upon by incorportating x-location as well as y-location to compensate for fisheye
        '''
        inch_per_pixel = -.00003*yPixel + 0.1275
        return pixelWidth*inch_per_pixel 

    def find_width_edges(self, new_frame):
        '''
        Finds width edges of plate coming down assembly line once plate crosses PIXEL_THRESH
        '''
        imout = new_frame

        #Subtract
        image = cv2.subtract(new_frame, self.width_subtract_image)

        #Threshhold image
        new_imager = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(new_imager, self.THRESH, 255, cv2.THRESH_BINARY)

        #Edge detect using contours finding
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            #c is an array of points where edges were detected
            c = np.array(contours, dtype=object)
        else:
            return new_frame

        # Extract x and y coordinates from the array (uses numpy arrays to increase speed)
        self.extractPlateEdges(c)

        #Write detected width in pixels
        detected_width = self.calcWidth()

        #Error check
        if (0 in self.bottom_left or 0 in self.bottom_right or 10000 in self.bottom_left or detected_width < self.SMALLEST_PLATE 
            or detected_width > self.LARGEST_PLATE):
            return imout

        #Increment width frames counter
        self.width_frames += 1

        #Draw detected dots
        imout = cv2.circle(imout, self.bottom_left, radius=5, color=(0, 255, 0), thickness=10)
        imout = cv2.circle(imout, self.bottom_right, radius=5, color=(0, 255, 0), thickness=10)

        #Relevant info calculated after enough frames of detection
        if (self.width_frames == 50):
            self.finalizeMeasurements(detected_width)
            
        #Plate pickup check, starts incrementing after 60 frames and if bottom_right point moves to the right atleast 8 inches
        if (self.width_frames > 60 and ((detected_width - self.width_final) > 8)):
            self.plate_moved_frames += 1
            self.previous_width = detected_width
        else:
            self.plate_moved_frames = 0
    
        #If above conditions have been met for atleast 10 consecutive frames we can consider the plate picked up
        if(self.plate_moved_frames > 10):
            self.plate_picked_up = True
            print("\nPlate picked up")

        #House keeping for new leading edge detect
        if self.plate_picked_up:
            self.resetVariables()
       
       # Return the final image with width points and width message drawn on.
        return imout
    
    def calcWidth(self):
        '''
        Calculate width in inches using linear equation that uses the y-pixel value to calculate inch/pixel ratio
        inch__per_pixel = -3E-05*width_y_location + 0.1248
        '''
        width_pixels = self.bottom_right[0] - self.bottom_left[0]
        width_y_location = (self.bottom_right[1] + self.bottom_left[1])/2
        detected_width = self.convertPixelWidthToInches(width_pixels, width_y_location)

        return detected_width
    
    def extractPlateEdges(self, c):
        '''
        Isolates the left and right points of the plate coming down the assembly line
        '''

        for c_arr in c:
            # Extract x and y coordinates from the array
            x = c_arr[:, :, 0].flatten()
            y = c_arr[:, :, 1].flatten()

            # Check if the points are in the bottom right range
            in_bottom_right_range = np.logical_and(
                np.logical_and(x > self.bottom_right[0], x < self.BOTTOM_RIGHT_RIGHT_BOUND),
                np.logical_and(y < self.LOWER_BOUND, y > self.PIXEL_THRESH)
            )

            # Update the bottom right point
            bottom_right_points = c_arr[in_bottom_right_range]
            if len(bottom_right_points) > 0:
                self.bottom_right = bottom_right_points[:, 0, :].max(axis=0)

            # Check if the points are in the bottom left range
            in_bottom_left_range = np.logical_and(
                np.logical_and(x < self.bottom_left[0], x > self.BOTTOM_LEFT_LEFT_BOUND),
                np.abs(y - self.bottom_right[1]) < self.VERTICAL_TRAVEL
            )

            # Update the bottom left point
            bottom_left_points = c_arr[in_bottom_left_range]
            if len(bottom_left_points) > 0:
                self.bottom_left = bottom_left_points[:, 0, :].min(axis=0)

    
    def finalizeMeasurements(self, detected_width):
        '''
        Grab official measurements once plate has settled.
        In the initial software version that is 50 frames, can be changed to something better later
        '''
        self.good_set_point_left = self.bottom_left 
        self.good_set_point_right = self.bottom_right
        self.width_final = detected_width
        self.width_set = True
        self.previous_width = detected_width
        print("\nDetected width: ", round(self.width_final, 2))
        self.center_dist = round(self.getPlateSkewCenter(), 2)
        print("Detected center skew: ", self.center_dist)

    def getPlateSkewCenter(self):
        """
        Gets the distance between the plates center and the center of the roller 
        Uses inch_per_pixel = -.00003*y_location + 0.1248 to get inch/pixel ratio
        """
        plate_center = [((self.good_set_point_right[0] + self.good_set_point_left[0]) // 2), 
                        ((self.good_set_point_right[1] + self.good_set_point_left[1]) // 2)]
        
        center_dist_pixel = plate_center[0] - self.ROLLER_CENTER[0]
        center_dist = self.convertPixelWidthToInches(center_dist_pixel, plate_center[1])

        return center_dist

    def getReferencePoint(self):
        '''
        Finds and returns coordinates of orange/red bumper to the left of bottom roller
        This is used to tell the crane where the plate edges are relative to a static location
        This is dependent on the camera having the bumper in view and relys on it being a specific color
        If anything is changed about it the hsv color bounds will need to be changed to compensate
        Finds the location from global BACKGROUND_IMAGE
        The location is the rightmost middle point of the bumper
        '''
        #Read image
        image = self.BACKGROUND_IMAGE 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        #Threshold for our orange/red bumper color in HSV color space
        light_orange = (0, 120, 120)
        dark_orange = (18, 255, 255)
        rgb_mask = cv2.inRange(image, light_orange, dark_orange)

        #Find largest contour of thresholded image
        contours, hierarchy = cv2.findContours(rgb_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(contours, key = cv2.contourArea)

        #Get average point of that contour
        sum_x = 0
        sum_y = 0
        n = c.ravel() 
        count = len(n) // 2
        i = 0

        for j in n : 
            if i % 2 == 0: 
                sum_x += n[i] 
                sum_y += n[i + 1] 
            i += 1

        avg_x = sum_x // count
        avg_y = sum_y // count

        return (avg_x, avg_y)
    
    def resetVariables(self):
            self.previous_lowest_point = 0
            self.width_set = False
            self.thresh_crossed = False
            self.bottom_left = [10000, 0]
            self.good_set_point_left = [0, 0]
            self.good_set_point_right = [0, 0]
            self.bottom_right = [0, 0]
            self.previous_frame = self.BACKGROUND_IMAGE
            self.plate_picked_up = False
            self.frames_thresh_crossed = 0
            self.width_final = 0
            self.width_frames = 0
            self.plate_moved_frames = 0
            self.previous_width = 0
            self.center_dist = 0
    
    def find_leading_edge(self, new_frame):
        '''
        Finds the leading edge and point of the plate coming down the assembly line
        When the plate crosses threshold value modify flag to stop rollers and activate width detection
        '''
        if self.thresh_crossed:
            return self.find_width_edges(new_frame)
        
        else:
            #Looking for leading edge

            #Load images
            imout = new_frame

            #Subtract and reassign previous_frame to new_frame for next iteration
            image = cv2.subtract(new_frame, self.previous_frame)
            self.previous_frame = new_frame

            #Threshhold image
            image_cvt = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, image_thresh = cv2.threshold(image_cvt, 50, 255, cv2.THRESH_BINARY)

            #Find lowest line and associated lowest point
            lowest_line = [0,0,0,0]
            edges = cv2.Canny(image_thresh, 75, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=25)
            if (lines is None): #Check for no lines being detected
                return new_frame
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if (y1 > lowest_line[1]):
                    lowest_line = line[0]

            #Draw lowest point
            lowest_point = lowest_line[0:2]
            if (lowest_line[3] > lowest_line[1]):
                lowest_point = lowest_line[2:4]
            imout = cv2.circle(new_frame, lowest_point, radius=5, color=(255, 0, 0), thickness=10)

            # First lowest point must be above a certain threshold if it is too low that means 
            # the algorithim is detecting a plate being moved
            if (self.previous_lowest_point == 0):#Means this is the first frame in lowest point detection
                if(lowest_point[1] > self.PLATE_START_BOUND): #Bad detect b/c plate is too low
                    self.previous_lowest_point = 0
                    return imout
                
            #Set the bacground frame we will use to subtract from width detect algorithm
            #Takes picture when new plate is just above the roller stop threshold
            #This removes the need to constantly manually update background image
            if (lowest_point[1] > (self.PIXEL_THRESH-100)):
                self.width_subtract_image = new_frame

            #Check if lowest_point has crossed designated PIXEL_THRESH and is in bounds
            if ((lowest_point[1] > self.PIXEL_THRESH)  and (lowest_point[0] < self.BOTTOM_RIGHT_RIGHT_BOUND) 
                and (lowest_point[0] > self.BOTTOM_LEFT_LEFT_BOUND)):
                self.frames_thresh_crossed += 1
            else:
                self.frames_thresh_crossed = 0

            #Checks if plate is moving down for consecutive frames
            if (lowest_point[1] > self.previous_lowest_point):
                self.plate_moving_down_frames += 1 
            else:
                self.plate_moving_down_frames = 0
            
            if (self.plate_moving_down_frames > 10):
                self.moved_down_flag = True

            #Lowest point must cross PIXEL_THRESH for FRAMES_THRESH_CROSSED BUFFER times consecutively to activate stop
            #Lowest point must also be lower than previous lower point in order to activate stop. 
            #This was added for the mutiple plate functionality to prevent plates moving horizontally activating the stop, 
            if ((self.frames_thresh_crossed > self.FRAMES_THRESH_CROSSED_BUFFER) 
                and (self.moved_down_flag)): #Thresh crossed enough time to activate stop
                self.activateStop()
                return self.find_width_edges(new_frame)
            
            else: #Threshold not crossed yet
                self.previous_lowest_point = lowest_point[1]
                return imout
