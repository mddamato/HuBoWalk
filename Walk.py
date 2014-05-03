import hubo_ach as ha
import ach
import sys
import time
from ctypes import *
import math

r = ach.Channel(ha.HUBO_CHAN_REF_NAME)

state = ha.HUBO_STATE()

ref = ha.HUBO_REF()
for arg in sys.argv:
    StepLengthInput=arg

StepLengthInput = .2 #testing

#initial eqns
l1=340.03
l2=340.38
l3=114.97
HipXPosition = (l1+l2+l3)*.75
HipYPosition = .5
FootAngle=0
leg=0
i=0
xw=HipXPosition-l3*math.cos(FootAngle)
yw=HipYPosition-l3*math.sin(FootAngle)
angle1=math.atan(yw/xw)-math.acos((l1**2-l2**2+xw**2+yw**2)/(2*l1*math.sqrt(xw**2+yw**2)))
angle2=math.pi-math.acos((l1**2+l2**2-xw**2-yw**2)/(2*l1*l2))
angle3=FootAngle-angle1-angle2
height=l1*math.cos(angle1)+l2*math.cos(angle2+angle1)+l3*math.cos(angle3+angle1+angle2)

#main function
def main():
	Crouch()
	LeanToLeft()
	LiftRightLeg()
	time.sleep(2)
	DropRightLeg()
	time.sleep(4)
	SlideRight()
	r.close()

#Slide right
def SlideRight():
	print("Slide Right")
	leanangle=math.asin(160/height)
	
	FootAngle=0
	xe=(l1+l2+l3)*.85
	ye=0
	xw=xe-l3*math.cos(FootAngle)
	yw=ye-l3*math.sin(FootAngle)

	RAngle1Lean=math.atan(yw/xw)-math.acos((l1**2-l2**2+xw**2+yw**2)/(2*l1*math.sqrt(xw**2+yw**2)))
	RAngle2Lean=2*math.atan(math.sqrt(((l1+l2)**2-(xw**2+yw**2))/(-1*(l1-l2)**2+(xw**2+yw**2))))
	RAngle3Lean=FootAngle-RAngle1Lean-RAngle2Lean

	RightHipMove = -(angle1)+RAngle1Lean
	RightKneeMove  = -angle2+RAngle2Lean
	Leanangle3R           = RAngle3Lean-angle3

	ye=float(.2)*10**3

	xw=xe-l3*math.cos(FootAngle)
	yw=ye-l3*math.sin(FootAngle)

	LAngle2Lean=2*math.atan(math.sqrt(((l1+l2)**2-(xw**2+yw**2))/(-1*(l1-l2)**2+(xw**2+yw**2))))
	LAngle1Lean=math.atan(yw/xw)-math.acos((l1**2-l2**2+xw**2+yw**2)/(2*l1*math.sqrt(xw**2+yw**2)))
	LAngle3Lean=FootAngle-LAngle1Lean-LAngle2Lean

	#calc angle differences
	LeftKneeMove  = -angle2+LAngle2Lean
	LeftHipMove   = -(angle1)+LAngle1Lean
	Leanangle3L   = LAngle3Lean-angle3
	
	#Slowly increment to final positions
	for l in range(0,1500):
		time.sleep(.003)
		ref.ref[ha.LHR]=ref.ref[ha.LHR]-leanangle/1500
		ref.ref[ha.RHR]=ref.ref[ha.RHR]-leanangle/1500
		ref.ref[ha.LAR]=ref.ref[ha.LAR]+leanangle/1500
		ref.ref[ha.RAR]=ref.ref[ha.RAR]+leanangle/1500
		ref.ref[ha.LKN]=ref.ref[ha.LKN]+LeftKneeMove/1500
		ref.ref[ha.RKN]=ref.ref[ha.RKN]+RightKneeMove/1500
		ref.ref[ha.LAP]=ref.ref[ha.LAP]+Leanangle3L/1500
		ref.ref[ha.RAP]=ref.ref[ha.RAP]+Leanangle3R/1500
		ref.ref[ha.LHP]=ref.ref[ha.LHP]+LeftHipMove/1500
		ref.ref[ha.RHP]=ref.ref[ha.RHP]+RightHipMove/1500
		r.put(ref)

#Drop Right Leg
def DropRightLeg():
	print("Drop Right Leg")
		
	xe=(l1+l2+l3)*.85
	ye=-float(.2)*10**3
	xw=xe-l3*math.cos(FootAngle)
	yw=ye-l3*math.sin(FootAngle)
	
	#same equations
	angle2lift=2*math.atan(math.sqrt(((l1+l2)**2-(xw**2+yw**2))/(-1*(l1-l2)**2+(xw**2+yw**2))))
	angle1lift=math.atan(yw/xw)-math.acos((l1**2-l2**2+xw**2+yw**2)/(2*l1*math.sqrt(xw**2+yw**2)))
	angle3lift=FootAngle-angle1lift-angle2lift

	angle2down=2*math.atan(math.sqrt(((l1+l2)**2-(xw**2+yw**2))/(-1*(l1-l2)**2+(xw**2+yw**2))))
	angle1down=math.atan(yw/xw)-math.acos((l1**2-l2**2+xw**2+yw**2)/(2*l1*math.sqrt(xw**2+yw**2)))
	angle3down=FootAngle-angle1down-angle2down

	LegmovementKnee=-angle2+angle2lift
	LegmovementHip=-(angle1)+angle1lift
	LegmovementAnkle=-(angle3)+angle3lift

	#
	for l in range(0,1500):
		time.sleep(.001)
		ref.ref[ha.RAP]=ref.ref[ha.RAP]+LegmovementAnkle/1500
		ref.ref[ha.RKN]=ref.ref[ha.RKN]+LegmovementKnee/1500
		ref.ref[ha.RHP]=ref.ref[ha.RHP]+LegmovementHip/1500
		r.put(ref)

#Lift Right Leg
def LiftRightLeg():
	print("Lift Right Leg")
		
	xe=(l1+l2+l3)*.6
	ye=0
	xw=xe-l3*math.cos(FootAngle)
	yw=ye-l3*math.sin(FootAngle)

	angle2lift=2*math.atan(math.sqrt(((l1+l2)**2-(xw**2+yw**2))/(-1*(l1-l2)**2+(xw**2+yw**2))))
	angle1lift=math.atan(yw/xw)-math.acos((l1**2-l2**2+xw**2+yw**2)/(2*l1*math.sqrt(xw**2+yw**2)))
	angle3lift=FootAngle-angle1lift-angle2lift

	LegmovementKnee=-angle2+angle2lift
	LegmovementHip=-(angle1)+angle1lift
	LegmovementAnkle=-(angle3)+angle3lift

	for l in range(0,1500):
		time.sleep(.001)
		ref.ref[ha.RAP]=ref.ref[ha.RAP]+LegmovementAnkle/1500
		ref.ref[ha.RKN]=ref.ref[ha.RKN]+LegmovementKnee/1500
		ref.ref[ha.RHP]=ref.ref[ha.RHP]+LegmovementHip/1500
		r.put(ref)

#Lean
def LeanToLeft():
	print("LeanToLeft")

	height=l1*math.cos(angle1)+l2*math.cos(angle2+angle1)+l3*math.cos(angle3+angle1+angle2)
	leanangle=math.asin(90/height)

	ref.ref[ha.LSR] = (math.pi)*.05
	ref.ref[ha.RSR]	= -(math.pi)*.05
	for l in range(0,1500):
		time.sleep(.001)
		ref.ref[ha.LHR]=ref.ref[ha.LHR]-leanangle/1500
		ref.ref[ha.RHR]=ref.ref[ha.RHR]-leanangle/1500
		ref.ref[ha.LAR]=ref.ref[ha.LAR]+leanangle/1500
		ref.ref[ha.RAR]=ref.ref[ha.RAR]+leanangle/1500
		r.put(ref)

#Crouch Down
def Crouch():
	print("Crouch")

	for l in range(0,1500):
		time.sleep(.001)
		ref.ref[ha.LKN]=ref.ref[ha.LKN]+angle2/1500
		ref.ref[ha.RKN]=ref.ref[ha.RKN]+angle2/1500
		ref.ref[ha.LAP]=ref.ref[ha.LAP]+(angle3)/1500
		ref.ref[ha.RAP]=ref.ref[ha.RAP]+(angle3)/1500
		ref.ref[ha.LHP]=ref.ref[ha.LHP]+(angle1)/1500
		ref.ref[ha.RHP]=ref.ref[ha.RHP]+(angle1)/1500
		r.put(ref)

main()
