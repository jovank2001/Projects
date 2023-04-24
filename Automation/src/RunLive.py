'''
Takes live image feed from camera 118 above shear layoff assembly line
Determines where the leading edge of the plate is and where the width edges of the plate are, 
as well as difference between center of plate and center of rollers

LIMITATIONS: -Program must be able to run at atleast 20 frames per second
             -Current Pixel values are for a 1920x1280 video feed, if this changes they will all need to be updated
             -Crane should not move below PIXEL_THRESH in cameras frame
             -plate_picked_up flag is approximate and activates when excessive movement by either the plate or shadows is detected,
              it should not be relyed on as a precise variable for monitoring the cranes exact movements.
             -Errors may occur if crane is moving over plate while it is coming down assembly line before it hits PIXEL_THRESH 
              (i.e dont block cameras view of plates leading edge with crane before it is stopped).
              They can move it anywhere else however (i.e. to drop off or move plates around wagon area)
             -Werid plate repositioning movements where plates are placed from wagon onto assembly line may cause errors
Written by Jovan Koledin for ENSC-41 Gonzaga Senior Design Project 2022-2023
'''
import time
import cv2
from PlateLocateLean import PlateLocate

# This is the source of the video stream.
# rtsp://<user>:<password>@<ip address>:<port>/
source = r'rtsp://rtsp.user:password@192.10.0.0:554/'
#Y Pixel value to stop rollers and activate width detection when crossed
PIXEL_THRESH = 920
#Picture of what camera sees with no plate in view. 
#Only needs to be reset if region in bounding box changes in appearence (See PlateLocate for bounding box)
BACKGROUND_PATH_VIDEO = '../Images/118_new_background.png'
#Path to where you want to save the processed video
OUT_VIDEO_PATH = '../output_videos/118_test2_cut2_56_out2.mp4'

#Captures the video stream from the source
cap = cv2.VideoCapture(source)

# Define the codec and create VideoWriter object
FPS = 20.0
RESOLUTION = (1920, 1280)
out = cv2.VideoWriter('output.mp4', 0x00000021, FPS, RESOLUTION)

# Capture video from default camera
cap = cv2.VideoCapture(0)

# Create Plate Locate object
Locate = PlateLocate(PIXEL_THRESH, BACKGROUND_PATH_VIDEO)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

# Process and save video
while cap.isOpened():
    # Read frame from camera
    ret, frame = cap.read()
    if ret:
        #Process frame
        out_frame = Locate.find_leading_edge(frame)

        # Write the processed frame to the output video file
        out.write(out_frame)

        # Display the processed frame
        cv2.imshow('Processed Video', out_frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()






