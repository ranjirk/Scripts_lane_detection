# Scripts_lane_detection
  Run datection.py with image file as argument.
    >>python detection.py img.jpg
  "new_image.png" will be generated with lane highlighted in translucent white.
Preprocess image by
  * Defining ROI

      Find a suitable region where the probability of lane ig high. This occurs mostly on bottom-center part of the image.
      With this focused image, unnecessary parts of image that usually include trees & anything that falls outside street can be neglected.
  * Thickened edges

      Find edge lines in the defined roi image. This will help in finding lines which will serve as lanes as they fall under lines category.
      Thickening it will enhance the lane lines & destroy curvy edges.
  * Detecting lines

    From this edge image, HoughlinesP function will get those lines that are to be considered as lane lines.
    These lines are validated in lineCalculation() where line length, angle, slope are calculated & filtered with conditions.
  * Segregation on lines

    Line of a lane that fall on left will have -ve slope, right has +ve slope. Categorising lines as left & right will help in building the lane region.
  * Defining & drawing lane region

    With all lines defferentiated as left/right, points for lane region is calculated. This will result in four points which is drawn on original image as lane with overlay.
