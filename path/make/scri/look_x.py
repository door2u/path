
def LookX___(owne, angl, axisRigh, math, mathutils):
	lookX___Acti = False
	if owne["lookX___"] == True:
		if axisRigh != 0.0:
			angl -= axisRigh
			# maximum mouse change. to prevent jumping that occurs when the mouse first enters a window
			lookX___Cut_ = owne["lookX___Cut_"]
			if math.fabs(axisRigh) <= lookX___Cut_:
				lookX___Acti = True
	return math.degrees(angl), lookX___Acti

