# ----------
# Background
#
# A robotics company named Trax has created a line of small self-driving robots
# designed to autonomously traverse desert environments in search of undiscovered
# water deposits.
#
# A Traxbot looks like a small tank. Each one is about half a meter long and drives
# on two continuous metal tracks. In order to maneuver itself, a Traxbot can do one
# of two things: it can drive in a straight line or it can turn. So to make a
# right turn, A Traxbot will drive forward, stop, turn 90 degrees, then continue
# driving straight.
#
# This series of questions involves the recovery of a rogue Traxbot. This bot has
# gotten lost somewhere in the desert and is now stuck driving in an almost-circle: it has
# been repeatedly driving forward by some step size, stopping, turning a certain
# amount, and repeating this process... Luckily, the Traxbot is still sending all
# of its sensor data back to headquarters.
#
# In this project, we will start with a simple version of this problem and
# gradually add complexity. By the end, you will have a fully articulated
# plan for recovering the lost Traxbot.
#
# ----------
# Part One
#
# Let's start by thinking about circular motion (well, really it's polygon motion
# that is close to circular motion). Assume that Traxbot lives on
# an (x, y) coordinate plane and (for now) is sending you PERFECTLY ACCURATE sensor
# measurements.
#
# With a few measurements you should be able to figure out the step size and the
# turning angle that Traxbot is moving with.
# With these two pieces of information, you should be able to
# write a function that can predict Traxbot's next location.
#
# You can use the robot class that is already written to make your life easier.
# You should re-familiarize yourself with this class, since some of the details
# have changed.
#
# ----------
# YOUR JOB
#
# Complete the estimate_next_pos function. You will probably want to use
# the OTHER variable to keep track of information about the runaway robot.
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
from robot import *
from math import *
from matrix import *
import random


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
# """
# def estimate_next_pos(measurement, OTHER = None):
#     Estimate the next (x, y) position of the wandering Traxbot
#     based on noisy (x, y) measurements.
#     OTHER VECTOR FORM:
#     [
#        X
#        Y
#        heading
#     ]
#     if OTHER == None:
#         OTHER = []
#         OTHER.append(measurement[0])
#         OTHER.append(measurement[1])
#         xy_estimate = measurement
#     else:
#         distance = distance_between((OTHER[0],OTHER[1]), measurement)
#         heading = acos((measurement[0]-OTHER[0])/distance)
#         if len(OTHER) == 2:
#             turn_angle = None
#             xy_estimate = measurement
#         else:
#             turn_angle = -(OTHER[2] - heading)

#             new_bot = robot(measurement[0],measurement[1], heading,turn_angle,distance)
#             new_bot.set_noise(0.,0.,0.)
#             new_bot.move_in_circle()
#             xy_estimate = (new_bot.x,new_bot.y)
#         OTHER.append(heading)
#         OTHER[0] = xy_estimate[0]
#         OTHER[1] = xy_estimate[1]

#     # You must return xy_estimate (x, y), and OTHER (even if it is None)
#     # in this order for grading purposes.
#     return xy_estimate, OTHER
# """

# def estimate_next_pos(measurement, OTHER = None):
#     """Estimate the next (x, y) position of the wandering Traxbot
#     based on noisy (x, y) measurements."""
#     """
#     OTHER VECTOR FORM:
#     [
#        [
#         X
#         Y
#        ]
#     ]
#     """
#     if OTHER == None:
#         OTHER = []
#         OTHER.append(measurement)
#         xy_estimate = measurement
#     elif len(OTHER) == 1:
#         OTHER.append(measurement)
#         xy_estimate = measurement
#     else:
#         OTHER.append(measurement)
#         distance = distance_between(OTHER[0], OTHER[1])
#         angle = 0
#         for i in range(2, len(OTHER)):
#             first = OTHER[i-2]
#             second = OTHER[i-1]
#             third = OTHER[i-0]
#             distance += distance_between(third, second)
#             angle+= angle_between([third[0]-second[0],third[1]-second[1]],[second[0]-first[0],second[1]-first[1]])
#         angle = angle /( len(OTHER)-1)
#         distance = distance /( len(OTHER)-2)
#         heading = atan2(third[1] - second[1], third[0] - second[0]) + angle
#         xy_estimate = (measurement[0] + distance * cos(heading), measurement[1] + distance * sin(heading))

#     # You must return xy_estimate (x, y), and OTHER (even if it is None)
#     # in this order for grading purposes.
#     return xy_estimate, OTHER
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    """
    OTHER VECTOR FORM:
    [
       [
        X
        Y
       ]
    ]
    """
    if OTHER == None:
        OTHER = []
        OTHER.append(measurement)
        xy_estimate = measurement
    elif len(OTHER) == 1:
        OTHER.append(measurement)
        xy_estimate = measurement
    else:
        OTHER.append(measurement)
        first = OTHER[-3]
        second = OTHER[-2]
        third = OTHER[-1]
        p1_dx = second[0]-first[0]
        p1_dy = second[1]-first[1]
        p2_dx = third[0]-second[0]
        p2_dy = third[1]-second[1]
        distance = distance_between(third, second)
        turn_angle = angle_between([p2_dx,p2_dy],[p1_dx,p1_dy])
        heading = atan2(p2_dy,p2_dx) + turn_angle
        est_x = measurement[0] + distance * cos(heading)
        est_y = measurement[1] + distance * sin(heading)
        xy_estimate = (est_x,est_y )

    # You must return xy_estimate (x, y), and OTHER (even if it is None)
    # in this order for grading purposes.
    return xy_estimate, OTHER

#this calculates the angle between 2 points using the law of cosines
def angle_between(p1, p2):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    return acos((x1*x2 + y1*y2) / (sqrt(x1**2 + y1**2) * sqrt(x2**2 + y2**2)))


"""
def angle_between(p1, p2):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[0]
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    return rads
"""


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
#     while not localized and ctr <= 10:
#         ctr += 1
#         measurement = target_bot.sense()
#         position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
#         target_bot.move_in_circle()
#         true_position = (target_bot.x, target_bot.y)
#         error = distance_between(position_guess, true_position)
#         if error <= distance_tolerance:
#             print "You got it right! It took you ", ctr, " steps to localize."
#             localized = True
#         if ctr == 10:
#             print "Sorry, it took you too many steps to localize the target."
#     return localized
import Tkinter
from turtle import Turtle

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
    while not localized and ctr <= 10:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 10:
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
test_target.set_noise(0.0, 0.0, 0.0)

demo_grading(estimate_next_pos, test_target)
