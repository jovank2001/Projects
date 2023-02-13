'''
Takes video feed or image from top down camera above assembly line
Determines where the leading edge of the plate is and where the width edges of the plate are
Written by Jovan Koledin for Kaiser Aluminum
'''
import utils

#Path to background image with which every subsequent image will be subtracted
BACKGROUND_PATH_VIDEO = '../Images/118_background_compressed.png' #Compressed to 1280X720 for video format
BACKGROUND_PATH_IMAGE = '../Images/118_background.png'
#Path to video you wish to process if processing video
VIDEO_PATH = '../test_videos/subtraction_video_test_118.mp4'
OUT_VIDEO_PATH = '../output_videos/leading_detection_test3.mp4'
PROCESS_VIDEO = True
#Path to image your wish to process if processing image
IMAGE_PATH = '../Images/118_with_plate.png'
OUT_IMAGE_PATH = '../Images/118_with_plate_edged_85.png'
PROCESS_IMAGE = False


if __name__ == '__main__':

    if PROCESS_VIDEO:
        utils.create_global_background(BACKGROUND_PATH_VIDEO)
        utils.create_global_previous(BACKGROUND_PATH_VIDEO)
        utils.process_video(VIDEO_PATH, OUT_VIDEO_PATH)
    
    elif PROCESS_IMAGE:
        utils.create_global_background(BACKGROUND_PATH_IMAGE)
        utils.create_global_previous(BACKGROUND_PATH_IMAGE)
        utils.process_image(IMAGE_PATH, OUT_IMAGE_PATH)






