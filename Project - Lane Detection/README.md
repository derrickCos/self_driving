# Methodology
Here we have implemented a very simple algorithm to detect the lanemarkings in the road using standard image processing techniques, following the following pipeline:

 1. First, the input image is preprocessed by color space transformation from RGB to HSV. After that, only the V channel (value) is selected for further processing. By doing so, we  extract information only about the illumination, making the implementation less sensitive to color differences. This way, the code worked perfectly both on white and yellow lines without any change.
 
 2. Gaussian blur. This reduces the noise in the image, in order to improve the edge detection step later on.
 
 3. Edges are extracted using the Canny edge detector. A region of interest is applied in order to remove non interesting lines. We assume that the vehicle is reasonably centered with respect to the lane.
 
 4. Next, straight lines are detected using the Hough transform.
 
 5. Finally, we create two sets of lines associated to the left and right lanemarkings, based on the slope of the lines. These sets are further averaged to create a single line (left and right). Finally, two single lines are drawn on the image, from the bottom of the image until the furthest detected point in the edges.
 
# Shortcomings

There are a few aspects that could be improved or that can potentially make the algorithm fail:
- Curved lanemarkings. Edge lines from Hough are detected using a linear model of the lanemarking. However a linear model does not hold for curved roads. The output from the Hough detector would be a piecewise-linear lanemarking. However we would need to be able to determine which sub-lines belong to the same lanemarking. A possible approach to curved lanes would be to parametrice the lanemarking as a quadratic curve or a Bézier curve. This would however require extending the Hough space to more dimensions (one per extra parameter), which would exponentially increase the computation time.

- Light/road conditions. It is likely that the code will perform worse under non-ideal lightning conditions. For example, with shadows or reflections on the road (e.g. with rain), which would make the edges be not so clear to the Canny detector. An autoexposure function could be implemented to improve image quality. Furthermore, the video has always featured clear front view from dashboard without any midsized cars obstructing the view. Obstructions such as another cars might change the result of the detection.

- Defined parameters. The code is quite tailor-made for this application, with a lot of tuning parameters: region of interest (ROI), Canny and Hough parameters, etc. This makes the algorithm very sensitive to different inputs. An apporach to improve this area will be to use machine learning to accommodate different situations.

- Centered-vehicle assumption. The region of interest (ROI) assumes that the vehicle is somewhat centered in the lane. This allows us to discard a big portion of the image and focus on extracting lines only where required. This provides a good performance but will make the algorithm fail if the vehicle is not well centered or if we are executing a lane change.
