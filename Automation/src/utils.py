'''
Utils library for Kaiser Plate detection
'''
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
import colorsys
from moviepy.editor import *


def create_global_background(background_path):
    '''
    Load background image into global variable a singular time 
    instead of doing it every iteration of find_edge_subtraction
    '''
    global background_image
    background_image = cv2.imread(background_path)

def process_video(test_video, output_video):
    """
    Read input video stream and produce a video file with detected lane lines.
        Parameters:
            test_video: Input video.
            output_video: A video file with detected lane lines.
    """
    input_video = VideoFileClip(test_video, audio=False)
    processed = input_video.fl_image(find_edge_subtraction)
    processed.write_videofile(output_video, audio=False)

def find_lines(n):
    '''
    Find leftmost and rightmost lines from given point coordinates
    Format for each line = [x1, y1, x2, y2]
    Returns: [line1, line2]

    '''
    #Assign specific edges of plate coordinates in arrays
    bottom_left = [10000, 0]
    top_left = [10000, 0]
    bottom_right = [0, 0]
    top_right = [0, 0]
    l = 0
    for k in n:
        if(l % 2 == 0):
            x = n[l]
            y = n[l + 1]

            if (x < bottom_left[0]):
                bottom_left[0] = x
                bottom_left[1] = y
        
            if (x > bottom_right[0]):
                bottom_right[0] = x
                bottom_right[1] = y

        l = l + 1

    l = 0
    for k in n:
        if(l % 2 == 0):
            x = n[l]
            y = n[l + 1]

            if (x > bottom_left[0] and x < top_left[0] and y < bottom_left[1]):
                top_left[0] = x
                top_left[1] = y
        
            if (x < bottom_right[0] and x > top_right[0] and y < bottom_right[1]):
                top_right[0] = x
                top_right[1] = y

        l = l + 1

    left_line = [bottom_left[0], bottom_left[1], top_left[0], top_left[1]]
    right_line = [bottom_right[0], bottom_right[1], top_right[0], top_right[1]]
    #Error check
    if (((right_line[0] - left_line[0]) < 50) or (0 in left_line) or (0 in right_line) or (right_line[2] - left_line[2] < 50)):
        return False
        print("No good lines detected")

    return [left_line, right_line]

def process_image(input_path, output_path):
    '''
    Take input image path and process with image subtraction edge detection method
    Return processed image to ouput path
    '''
    image = cv2.imread(input_path)
    processed_image = find_edge_subtraction(image)
    cv2.imwrite(output_path, processed_image)

def find_edge_subtraction(new_frame):
    '''
    Subtract new frame from background image and find the bounding box of image difference
    Draws lines over new_frame and returns drawn over image
    '''
    
    #Load images
    im2 = new_frame
   
    #Subtract
    image = cv2.subtract(new_frame, background_image)

    #Threshhold image
    new_imager = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(new_imager, 85, 255, cv2.THRESH_BINARY)

    #Find largest contour
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        #Find coordinates of edges
        approx = cv2.approxPolyDP(c, 0.009 * cv2.arcLength(c, True), True)
        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel() 
    #If no contours detected
    else:
        return im2
    #If contours detected dont have atleast 4 points
    if len(n) < 8:
        return im2
    
    #Find and draw width edges of plate
    lines = find_lines(n)
    #Check if lines are valid (if plate not valid)
    if (lines == False):
        return im2

    #Draw detected lines
    left, right = lines
    left_first_coor = [left[0], left[1]]
    left_second_coor = [left[2], left[3]]
    right_first_coor = [right[0], right[1]]
    right_second_coor = [right[2], right[3]]
    imout = cv2.line(im2, left_first_coor, left_second_coor, (0,255,0), 5)
    imout = cv2.line(imout, right_first_coor, right_second_coor, (0, 255, 0), 5)

    # Return the final image with edges drawn on.
    return imout
 