# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position.
#
# ----------
# GRADING
#
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
# def KalmanFilter(x,P,Z,u,F,H,R,I):
#     #code derived from lectures here:
#     #https://www.udacity.com/course/viewer#!/c-cs373/l-48723604/e-48724495/m-48687710
#     #prediction
#     x = (F*x) + u
#     P = F * P * F.transpose()

#     #measurement update
#     y  = Z - (H*x)
#     S = (H*P*H.transpose())+R
#     K = P*H.transpose()*S.inverse()
#     x = x + (K*y)
#     P = (I -(K*H))*P

#     return(x,P)


# def estimate_next_pos(measurement, OTHER = None):
#     """Estimate the next (x, y) position of the wandering Traxbot
#     based on noisy (x, y) measurements."""
#     #if other = none this is the first time this is run.
#     #will be in the form: x,y,heading, distance, turning-angle
#     #based on tutorial here:
#     #http://nbviewer.ipython.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/table_of_contents.ipynb
#     dimx = 4 #because if position and velocity in 2 diminsions, it will need to be 4
#     dimz = 2 #if there are only positions xy this should be 2

#     ###setting up the matrices
#     posx = measurement[0]
#     posy = measurement[1]
#     I = matrix([[1., 0., 0., 0.], #state transition function
#                 [0., 1., 0., 0.],
#                 [0., 0., 1., 0.],
#                 [0., 0., 0., 1.]])
#     if OTHER == None: #first time this is running
#         OTHER = []
#         x = matrix([[posx],[posy],[0],[0]])#this starts the initial measurement
#         P = I
#     else:
#         x = OTHER[0]
#         P = OTHER[1]
#     Z = matrix([[posx],[posy]])#this starts the initial measurement
#     u = matrix([[0],[0],[0],[0]])
#     F = matrix([[1., 0., 1, 0.], #state transition function
#                 [0., 1., 0., 1],
#                 [0., 0., 1., 0.],
#                 [0., 0., 0., 1.]])
#     H = matrix([[1,0,0,0],[0,1.,0,0]])#meansurement matrix
#     R = matrix([[.00001,0],[.00001,1.]])#uncertainty matrix
#     #I = matrix([[]]).identity(dimx)#identity matrix

#     x,P = KalmanFilter(x,P,Z,u,F,H,R,I)
#         ##this xy estimate should be
#     OTHER = [x, P]
#     xy_estimate = (x.value[0][0], x.value[1][0])
#     # You must return xy_estimate (x, y), and OTHER (even if it is None)
#     # in this order for grading purposes.
#     return xy_estimate, OTHER

def mean(lists):
    sums = 0
    for i in range(len(lists)):
        sums += lists[i]
    return sums/len(lists)

def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    """
    OTHER VECTOR FORM:
    [
       previousPoint (x,y) # this is the previous measurement,
       prev_heading (int) # this is the heading - the turn angle,
       distance_between_array([])
   ]
    """
    if OTHER == None:
        OTHER = {}
        OTHER["previous_point"] = (0.0,0.0)
        OTHER["previous_heading"] = 0
        OTHER["distance_between_array"] = []

    previous_heading = OTHER["previous_heading"]
    previous_point = OTHER["previous_point"]#retrieving the previous point to use later
    distance_between_array = OTHER["distance_between_array"]

    dx = measurement[0] - previous_point[0]
    dy = measurement[1] - previous_point[1]
    aR = atan2(dy,dx)
    distance_between_array.append(distance_between(previous_point,measurement))
    mean_distance = mean(distance_between_array)

    turn_angle = aR - previous_heading
    heading = aR + turn_angle
    est_x = measurement[0] + mean_distance * cos(heading)
    est_y = measurement[1] + mean_distance * sin(heading)

    OTHER["previous_point"] = measurement #storing the measurement as the previous point
    OTHER["previous_heading"] = aR
    OTHER["distance_between_array"] = distance_between_array
    xy_estimate = (est_x,est_y )
    # You must return xy_estimate (x, y), and OTHER (even if it is None)
    # in this order for grading purposes.
    return xy_estimate, OTHER

#this calculates the angle between 2 points using the law of cosines
def angle_between(p1, p2):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    return acos((x1*x2 + y1*y2) / (sqrt(x1**2 + y1**2) * sqrt(x2**2 + y2**2)))

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any
# information that you want.
# def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
#     localized = False
#     distance_tolerance = 0.01 * target_bot.distance
#     ctr = 0
#     # if you haven't localized the target bot, make a guess about the next
#     # position, then we move the bot and compare your guess to the true
#     # next position. When you are close enough, we stop checking.
#     while not localized and ctr <= 1000:
#         ctr += 1
#         measurement = target_bot.sense()
#         position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
#         target_bot.move_in_circle()
#         true_position = (target_bot.x, target_bot.y)
#         error = distance_between(position_guess, true_position)
#         if error <= distance_tolerance:
#             print "You got it right! It took you ", ctr, " steps to localize."
#             localized = True
#         if ctr == 1000:
#             print "Sorry, it took you too many steps to localize the target."
#     return localized
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    import turtle    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 25.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.1, 0.1, 0.1)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.1, 0.1, 0.1)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(0.1, 0.1, 0.1)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 1000:
            print "Sorry, it took you too many steps to localize the target."
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
    return localized
# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading(estimate_next_pos, test_target)




