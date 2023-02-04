'''
Takes video feed or image from top down camera above assembly line
Draws over the camera feed with edges of detected plate
Prints width of detected plate
Written by Jovan Koledin for Kaiser Aluminum
'''
import utilsExtend
import utils

#Path to background image with which every subsequent image will be subtracted
BACKGROUND_PATH_VIDEO = '../Images/118_background_compressed.png' #Compressed to 1280X720 for video format
BACKGROUND_PATH_IMAGE = '../Images/118_background.png'
#Path to video you wish to process if processing video
VIDEO_PATH = '../test_videos/subtraction_video_test_118.mp4'
OUT_VIDEO_PATH = '../output_videos/subtraction_video_test_118_out.mp4'
PROCESS_VIDEO = False
#Path to image your wish to process if processing image
IMAGE_PATH = '../Images/118_with_plate.png'
OUT_IMAGE_PATH = '../Images/118_with_plate_edged_85.png'
PROCESS_IMAGE = True


if __name__ == '__main__':

    if PROCESS_VIDEO:
        utils.create_global_background(BACKGROUND_PATH_VIDEO)
        utils.process_video(VIDEO_PATH, OUT_VIDEO_PATH)
    
    elif PROCESS_IMAGE:
        utils.create_global_background(BACKGROUND_PATH_IMAGE)
        utils.process_image(IMAGE_PATH, OUT_IMAGE_PATH)






