
def LookY___(owne, angl, axisUp__, math, mathutils):
	lookY___Acti = False
	if owne["lookY___"] == True:
		if axisUp__ != 0.0:
			lookY___Cut_ = owne["lookY___Cut_"]
			if math.fabs(axisUp__) <= lookY___Cut_:
				angl -= axisUp__
				lookY___Limi = owne["lookY___Limi"]
				if lookY___Limi == True:
					lookY___LimiInve = owne["lookY___LimiInve"]
					lookY___LimiUppe = owne["lookY___LimiUppe"]
					lookY___LimiLowe = owne["lookY___LimiLowe"]
					if lookY___LimiInve == True:
						# high limit
						if angl < 0.0:
							lookY___LimiLowe = -math.pi / 2.0
						# low limit
						else:
							lookY___LimiUppe = math.pi / 2.0
					# high limit
					if angl > lookY___LimiUppe:
						angl = lookY___LimiUppe
					# low limit
					if angl < lookY___LimiLowe:
						angl = lookY___LimiLowe
			lookY___Acti = True
	return math.degrees(angl), lookY___Acti

