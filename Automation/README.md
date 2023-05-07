# ENSC41-Pick-and-Place: Senior Design Project for Pick and Place Technology

## 1. Overview
This repository contains a collection of Python scripts that can identify and localize aluminum plates and wagons from top down cameras.
Written by Gonzaga Univeristy Senior Design Team ENSC-41 (Jovan Koledin, Ethan Higa, Dylan Brown, and Jason Dhanota)
NOTE: All code in this repository was written by Jovan Koledin
Customer: Kaiser Aluminum

## 2. Features

### Design Methodology
In order to locate the plates coming down the assembly line, new frames from top down cameras are subtracted from previous frames. The results of this subtraction are then analyzed, if a plate is coming down the assembly line the difference between the two frames will show up as the plate since the backgound are for the most part static.

### Moviepy Methods
Using functions:
* `ret_video = VideoFileClip(video_path, audio=False)` to obtain a video object. [VideoFileClip](https://moviepy-tburrows13.readthedocs.io/en/improve-docs/ref/VideoClip/VideoFileClip.html).
* `processed_video = ret_video.fl_image(function_apply_frame)` to apply the specified function of each frame of the video to make a new video . [Classes of Video Clips](https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html).
* `processed_video.write_videofile(video_path, audio=False)` to write video to path . 

### OpenCV Methods
* `sub_image = cv2.subtract(image_1, image_2)` to for instance subtract pixel values from `image_1` and `image_2`. [Image Arithmetic](https://docs.opencv.org/3.4/dd/d4d/tutorial_js_image_arithmetics.html)
* `ret_bool, thresh_image = cv2.threshold(image, thresh_val, max_val, cv2.THRESH_BINARY)` will set pixel values in `thresh_image` to `0` or `max_val` if above or below `thresh_val`. [Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html).
* `contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)` to find the contours with `RETR_EXTERNAL` to retrieve only the extreme outer contours and `CHAIN_APPROX_SIMPLE` to return only four points of the found contour. [Contours](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html). 
* `edges = cv2.Canny(thresh_image, thresh1, thresh2)` to get the gradient, changes in value, of the `thresh_image`. Gradient values that are in between `thresh1` and `thresh2` are outputted as `edges`. [Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html). 
* `lines = cv2.HoughLinesP(edges, rho, theta, threshold,  maxLineGap=num)` to detect straight lines set by `rho` and `theta` and that are `>threshold`. [Hough Line Transform](https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html). 
* `image_bright = cv2.convertScaleAbs(image,alpha,beta)` to change the brightness of the image, alpha scales the pixle values in the image, beta adds to the pixel values in the image. Returns adjusted image pixel values. [Operations on Arrays](https://docs.opencv.org/4.7.0/d2/de8/group__core__array.html)
* `image_blur = cv2.GaussianBlur(image, (kernel_size,kernel_size), 0)` to apply a Gaussian filter to the image with the given `kernel size`. A greater `kernel size` will provide an `image_blur` with a larger blur. [Image Filtering](https://docs.opencv.org/4.7.0/d4/d86/group__imgproc__filter.html)
* `image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)` to convert a bgr `image` to gray. `cv2.COLOR_BGR2GRAY` can be replaced with other color conversion codes for different converted outputs.  [Color Space Conversions](https://docs.opencv.org/4.7.0/d8/d01/group__imgproc__color__conversions.html)

## 3. Performance

### Accuracy
* Able to detect plate width within +/- 1.195 inches. 
* NOTE: Center skew values have not been tested
* NOTE 2: Plate width detection has seen limited testing
### Speed
* On a Windows PC with CORE i5 8th Gen the RunStatic code runs at ~30 fps depending on video clip. 

## 4. Software Framework and Tooling

* [RunStatic.py] for setting paths for input and output videos and images for processing as well as the pixel threshold for when to call the width detection. 
* [PlateLocateRaw.py] containing functions for video and image processing such as for finding the width and leading edge of the moving plate. Also where to set width pixel locations and where to recalibrate if input stream/videos are not 1920x1080 resolution.
## 5. Running the Code

### Instructions to Setup Software Environment
1. Download [git](https://git-scm.com/downloads) and [Python3](https://www.python.org/downloads/) to computer
2. [Setup ssh keys for Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
2. Enter command `git clone git@github.com:ENSC41/ENSC41-Pick-and-Place.git`
3. Enter command `pip install -r requirements.txt` to install all the dependencies for this project. 

### Instructions to Run Plate Detection on exististing (static) video
1. Enter `cd ENSC41-Pick-and-Place/Subtraction`
2. Enter editor to [RunStatic.py](https://github.com/ENSC41/ENSC41-Pick-and-Place/blob/main/src/RunStatic.py)
3. Inside the file set the `PROCESS_VIDEO` and `PROCESS_IMAGE` boolean if wanting to process videos or images
4. Upload an image from camera with no plate to the [/Images/] folder
5. Set the path to that image in the variables `BACKGROUND_PATH_VIDEO='../Images/<background.png>'`along with `BACKGROUND_PATH_IMAGE`
6. Upload a video to be processed to the [/test_videos/] folder or a image to processed to the [ENSC41/Pick-and-Place/Images](https://github.com/ENSC41/ENSC41-Pick-and-Place/tree/main/Images) folder
7. Set the path to that video to be processed `VIDEO_PATH = '../test_videos/<in_vid.mp4>` or image to be processed `IMAGE_PATH = '../Images/<in_pic.png>'`
8. Set the path to where the video should be outputted `OUT_VIDEO_PATH = '../output_videos/<out_vid.mp4>'` or image to be processed `OUT_IMAGE_PATH = '../Images/<out_img.png>'`
9. Edit constants inside PlateLocateRaw.py to ensure properly calibrated pixel locations
   - NOTE: ^ If PlateLocate class is not receiving frames in 1920X1280 resolution these will all need to be calibrated accordingly ^
   - NOTE 2:  ^^ If you are not using camera 118 or it has been moved at all these will all need to be calibrated accordingly ^^
10. Enter command `python RunStatic.py`

