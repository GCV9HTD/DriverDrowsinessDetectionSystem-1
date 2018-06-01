###  Omar Mustafa  ###
##  ID: 131 02 082  ##
######################
import numpy as np
import cv2
import dlib
import imutils
import csv
import argparse
import time
import math
import os
import playsound
import pygame
from imutils import face_utils
from time import gmtime, strftime
from scipy.spatial import distance as dist
from threading import Thread

#ANSI color codes,
#opening code: \033[ 'value' + m
#values: Black(30), Red(31), Green(32), Yellow(33), Blue(34), Magenta(35)
#        Cyan(36), White(37)
#Reset All: \033[0m

#smileCascade = cv2.CascadeClassifier("/home/omar/Desktop/HaarCascades/haarcascade_smile.xml")

#Assigning a path for the 'dat' file for 68 point face landmark predictor
PREDICTOR_PATH = "/home/omar/Desktop/shape_predictor_68_face_landmarks.dat"

FULL_POINTS = list(range(0, 68))
FACE_POINTS = list(range(17, 68))

JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_POINTS = list(range(27, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
MOUTH_OUTLINE_POINTS = list(range(48, 61))
MOUTH_INNER_POINTS = list(range(60, 68))
##############################################################
# NOTE THAT MOUTH_INNER_POINTS ORIGINAL RANGE IS ...(61, 68) #
#     THIS WAS CHANGED TO ...(60, 68), SO THE CODE CAN       #
#                 DETECT THE INNER MOUTH!                    #
##############################################################

#Constructing the argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--alarm", type=str, default="", help="path to alarm .WAV file")
args = vars(ap.parse_args())

#The Eye Aspect Ratio default value is "0.23"
#The Eye Aspect Ratio Consecutive Frames default value is "3"
#The Eey Aspect Ratio Consecutive Frames for Sleepiness default is "45"
EAR_THRESH = 0.20
EAR_CONSEC_FRAMES = 3
EAR_CONSEC_FRAMES_SLEEPY = 35

#Defining default values for blink counter
EAR_COUNTER = 0
TOTAL_EAR = 0
drowsy_COUNTER = 0

#The Mouth Aspect Ratio default value is "0.75"
#The Mouth Aspect Ratio Consecutive Frames default value is "3"
MAR_THRESH = 0.55
MAR_CONSEC_FRAMES = 15

#Defining default values for yawn counter
MAR_COUNTER = 0
TOTAL_MAR = 0

#Initialize boolean for alarm
ALARM_ON = False

#Detecting if yawn takes place between MIN & MAX thresholds
a = 0
a_COUNTER_MIN = 15
a_COUNTER_MAX = 30
b = 0

#defining the EYE ASPECT RATIO
def eye_aspect_ratio(eye):
  # compute the euclidean distances between the two sets of
  # vertical eye landmarks (x, y)-coordinates (which is [p2 - p6]
  #                                               and   [p3 - p5] )
  A = dist.euclidean(eye[1], eye[5])
  B = dist.euclidean(eye[2], eye[4])

  # compute the euclidean distance between the horizontal
  # eye landmark (x, y)-coordinates (which is [p1 - p4] )
  C = dist.euclidean(eye[0], eye[3])

  # compute the eye aspect ratio
  ear = (A + B) / (2.0 * C)
  #p = print(ear)

  # return the eye aspect ratio
  return ear

def mouth_aspect_ratio(mou):
  # compute the euclidean distances between the three sets of
  # vertical inner mouth landmarks (x, y)-coordinates (which is [p2 - p8]
  #                                                        and  [p3 - p7]
  #                                                        and  [p4 - p6] )
  A = dist.euclidean(mou[1], mou[7])
  B = dist.euclidean(mou[2], mou[6])
  C = dist.euclidean(mou[3], mou[5])

  # compute the euclidean distance between the horizontel
  # mouth landmark (x, y)-coordinates (which is [p1 - p5] )
  D = dist.euclidean(mou[0], mou[4])

  # compute the Mouth Aspect Ratio
  mar = (A + B + C) / (2.0 * D)
  # return the Mouth Ratio
  return mar

def alarm_sound(path):
  #play local alarm sound
  #playsound.playsound(path)
  pygame.mixer.init()
  pygame.mixer.music.load(path)
  pygame.mixer.music.play()

def laughter(lau):
  # compute the euclidean distance between horizontel outer
  # mouth landmarks (x, y)-coordinates (which is [p1 - p7] )
  A = dist.euclidean(lau[0], lau[6])
  # returns the Distance
  return A

#Loading the detector from Dlib, and predictor from local directory
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

###################################
### Either Video file or Camera ###
###################################
# Start capturing Video file
cap = cv2.VideoCapture('/home/omar/Desktop/TestVideos/part1.mp4')

# Start capturing WebCam
#cap = cv2.VideoCapture(0)

###Get the frames of video in number###
#fps = cap.get(cv2.CAP_PROP_FPS)
framecount = 0

while True:
	ret, frame = cap.read()
	framecount += 1
	frame = imutils.resize(frame, width = 800)

	if ret:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		rects = detector(gray, 0)

		for rect in rects:
			x = rect.left()
			y = rect.top()
			x1 = rect.right() - x
			y1 = rect.bottom() - y

			landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])

			left_eye = landmarks[LEFT_EYE_POINTS]
			right_eye = landmarks[RIGHT_EYE_POINTS]

			face_points = landmarks[FULL_POINTS]
			inner_mouth = landmarks[MOUTH_INNER_POINTS]
			outer_mouth = landmarks[MOUTH_OUTLINE_POINTS]
			#wrapping the points for each eye and both inner and outer mouth points
			left_eye_hull = cv2.convexHull(left_eye)
			right_eye_hull = cv2.convexHull(right_eye)
			inner_mouth_hull = cv2.convexHull(inner_mouth)
			outer_mouth_hull = cv2.convexHull(outer_mouth)
			# drawing the contours on frame
			cv2.drawContours(frame, [left_eye_hull], -1, (0, 0, 255), 1)
			cv2.drawContours(frame, [right_eye_hull], -1, (0, 0, 255), 1)
			cv2.drawContours(frame, [inner_mouth_hull], -1, (255, 0, 0), 1)
			cv2.drawContours(frame, [outer_mouth_hull], -1, (0, 255, 255), 1)
			# computing the Eye aspect ratio
			ear_left = eye_aspect_ratio(left_eye)
			ear_right = eye_aspect_ratio(right_eye)

			#Get the average of both eyes
			EAR = (ear_left + ear_right) / 2.0

			#Computing the Mputh Aspect ratio
			MAR = mouth_aspect_ratio(inner_mouth)

			if EAR < EAR_THRESH:
				EAR_COUNTER += 1
			else:
				if EAR_COUNTER >= EAR_CONSEC_FRAMES:
					TOTAL_EAR += 1

				EAR_COUNTER = 0

			if EAR < EAR_THRESH:
				drowsy_COUNTER += 1

				if drowsy_COUNTER >= EAR_CONSEC_FRAMES_SLEEPY:

					if not ALARM_ON:
						ALARM_ON = True

						if args["alarm"] != "":
							t = Thread(target=alarm_sound,args=(args["alarm"],))
							t.deamon = True
							t.start()

					cv2.putText(frame, "DROWSINESS ALERT!!!", (10,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

			else:
				drowsy_COUNTER = 0
				ALARM_ON = False


			if MAR > MAR_THRESH:
				MAR_COUNTER += 1
				a += 1
			else:
				if MAR_COUNTER >= MAR_CONSEC_FRAMES:
					TOTAL_MAR += 1
					a = 0
				MAR_COUNTER = 0

			if a >= a_COUNTER_MIN and a <= a_COUNTER_MAX:
				b = 1
			else:
				b = 0

			cv2.putText(frame, "Yawns: {}".format(TOTAL_MAR), (600, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
			cv2.putText(frame, "Blinks: {}".format(TOTAL_EAR), (600, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,225,205), 2)

			val1 = framecount
			val2 = "{:.3f}".format(EAR)
			val3 = "{:.3f}".format(MAR)

			xCent = x + x1/2
			yCent = y + y1/2

			print(val1, val2, val3, b)

			if xCent < 400:
				print("1",val1, val2, val3, xCent, yCent)
			else:
				print("2",val1, val2, val3, xCent, yCent)

			cv2.putText(frame, "E.A.R : {:.2f}".format(EAR), (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "Frames: {}".format(framecount), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
			cv2.putText(frame, "M.A.R : {:.2f}".format(MAR), (600, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

		cv2.imshow("Faces", frame)

	ch = 0xFF & cv2.waitKey(1)

	if ch == ord('q'):
		break

cv2.destroyAllWindows()
