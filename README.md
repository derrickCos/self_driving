# Discrete Localization :

Illustrated with discrete spots of 5 doors [] [] [] [] []

First you have inital BELIEF (probability of object in all locations are in MAXIMUM state of confusion = UNIFORM distribution): [0.2][0.2][0.2][0.2][0.2]

This is then followed by measurement by SENSING the location surrounding it and gives us the information about its location (this information is not exact and has uncertainty/probability)

Then robot will undergo motion and it carries the LESS probability from its previous location

The probability from the previous location will be added to the probability sensed at the new location after motion = CONVOLUTION

Localization alternates between cycle of SENSE and MOVE. 
MOVE will LOSE information becauuse robot motion is always uncertain.
SENSE will GAIN information because robot checks its surroundings.
CONVOLUTION from new measurement / SENSE then happens between the probability before and after move to create a better POSTERIOR
POSTERIOR will have  REDUCED uncertainty at every locations which means: 
		
	1. true postiive location probablity to be higher than the previous
	2. true negative location lower than previous (negative refers to where doors are located but robot is not there)


# 1-D Kalman Filter:
Kalman Filter is continuous and unimodal meaning that the graph has only one bump on the mean value.
The efficiency is quadratic and not exponential meaning the VARIANCE matrix is in terms of quadratic power. 
	this is good because the more dimension vector added to the filter the larger the variance.
	Number of computation steps are also quadratic given a fixed space of vectors

Measurements and followed by prediction to prepare for the next measurement

MEAN refers to the location in the one dimension (x-coord) 
VAR refers to the uncertainty that object is at the MEAN location

The gauss distribution describes how that there are probabilites that the object is NOT at its desired location

Measurements: with more and more measurements VARIANCE will always be less than the initial and the measured's VAR
Predict: when an robot is told to move by a certain steps, the movement always come with its own gaussian distribution of mean and variance
	 the predicted location's MEAN will be the sum of the initial location mean and the final location mean. 
	 The same applies to the VAR (new variance is sum of inital and motion's variance) 


# Particle Filter: 

- further accurately determine position of robot
-at first number of particles are spread evenly in a room.
	the filter need to create a process where the particles in the room must not only survive (remain in the room) but also ultimately follow where the robot is moving.
- A good particle filter will have all the particles clustered in the robot.
- Robot movement is commanded in a 360 degree space with x-axis being horizonatal and y-axis being vertical
- Noise (movement, turn and sensing) need to be manually adjusted according to the room the robot is placed in
- Process of Resampling:
	1. calculate position of robot relative to few landmarks in the area = MEASUREMENT
	2. generate random set of particles with random orientation and x y location
	3. move the random particles a set of distance and orientation
	4. **Allocate IMPORTANCE weights to the random particles:
		- Calcul: |Measurement - distance of new particles to landmark|
		- the LARGER the value will mean that the further the particle is from the robot and thus have higher IMPORTANCE to be RESAMPLED
		- RESAMPLED meaning that the 'bad' particle will be replaced with another random particle(s) (the number of replacements can vary)
		- ANY PARTICLE HAS PROBABLITY TO BE RESAMPLED REGARDLESS OF ITS IMPORTANCE WEIGHT
	5. compute error sum of particles against robot
	6. repeat 3 to 6 until error is below threshold

- Orientation does matter because depending on the orientation  of initial set of particles, the actual distance of particles to landmark after movement can differ

# Search Function:

Initialize robot paths as discrete nodes:

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
	
With '1' meaning path is blocked while '0' means path is free. 

Search function will expand each individual nodes to the surrounding nodes. With each path taken 'g' value increases. Overlaying with stochastic grid value 'f' you can get [y = g + f]

stochastic = [[1, 2, 3, 4],
       	      [2, 3, 4, 5],
              [3, 4, 5, 6],
              [4, 5, 6, 7]]

Path(s) that lead to goal with smallest 'y' value is the desired path

# PID Control

Due to nature of steering angle, robot tends to oscillate along a horizontal line. Imagine a horizontal x axis, as the robot tends to get closer to the axis, the robot will overshoot. Using PID control to adjust steering angle using the formula:

steer = - tau_p * CTE - tau_d * (cte_(t) - cte_(t-1)) * - tau_i * (sum of CTE)

*Cte refers to crosstrack error meaning the distance from axis to the robot

the first term will cause robot to move towards the axis, but will cause oscillation. the middle term (derivative of cte) will result in smooth oscillation however, error bias still remain due to the CTE. the last term will eliminate error bias and place the robot close to the x axis


