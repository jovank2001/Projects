Software pacakge being developed for Kaiser Aluminum to help them automate their layoff cranes.
Takes video stream input from 1920x1280 60fps Bosch Flexidome security cameras 
and locates Aluminum plates coming down assembly lines. Location is the position of the leading edge of each plate,
and the positions of the two width edges of the plate. PLCs from crane takes these measurements and use them to pickup 
plates and place them onto drop off wagons. 

The main idea behind the plate detection:

Subtract background image from every new frame->Apply binary threshold to image->Apply Canny edge detection->If edges are detected than we have a plate in frame->Locate the leftmost and rightmost edges.
(See main.py for pathing details if you wish to try with own videos or images)
