'''
Takes existing video or image from camera 118 above shear layoff assembly line
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
from PlateLocateRaw import PlateLocate

#Y Pixel value to stop rollers and activate width detection when crossed
PIXEL_THRESH = 920
#Picture of what camera sees with no plate in view. 
#Only needs to be reset if region in bounding box changes in appearence (See PlateLocate for bounding box)
BACKGROUND_PATH_VIDEO = '../Images/118_new_background.png'
BACKGROUND_PATH_IMAGE = '../Images/118_new_background.png'
#Path to video you wish to process if processing video
VIDEO_PATH = '../test_videos/MultiplePlateTest.mp4'
OUT_VIDEO_PATH = '../output_videos/MultiplePlateTest_out9.mp4'
PROCESS_VIDEO = True
#Path to image your wish to process if processing image
IMAGE_PATH = '../Images/118_map1_plate3.png'
OUT_IMAGE_PATH = '../Images/188_map1_plate3_out.png'
PROCESS_IMAGE = False

if __name__ == '__main__':
    
    if PROCESS_VIDEO:
        Locate = PlateLocate(PIXEL_THRESH, BACKGROUND_PATH_VIDEO)
        Locate.process_video(VIDEO_PATH, OUT_VIDEO_PATH)
        
    elif PROCESS_IMAGE:
        Locate = PlateLocate(PIXEL_THRESH, BACKGROUND_PATH_IMAGE)
        Locate.process_video(IMAGE_PATH, OUT_IMAGE_PATH)







