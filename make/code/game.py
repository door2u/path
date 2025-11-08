
def JoysNorm(valu, thre, maxi):
	if valu < 0:
		valu += thre
	else:
		valu -= thre
	valu /= (maxi - thre)
	return valu

def Inpu(variDict, owne, W, A, S, D, W_T, A_T, S_T, D_T, LEFT_SHIFT, RIGHTAXIS, UPAXIS, joysAxisRigh, joysAxisUp__, look, bge, math):
	up__ = 0.0
	righ = 0.0
	keyb = owne["keyb"]
	joys = owne["joys"]
	keybActi = True
	magn = 0.0
	if joys == True:
		maxi = 2 ** 15 - 1
		thre = owne["joysThre"]
		if RIGHTAXIS.positive:
			keybActi = False
			righ = JoysNorm(RIGHTAXIS.axisSingle, thre, maxi)
		else:
			righ = 0.0
		if UPAXIS.positive:
			keybActi = False
			up__ = JoysNorm(-1.0 * UPAXIS.axisSingle, thre, maxi)
		else:
			up__ = 0.0
	if keyb == True:
		inpuRighPrev = owne["inpuRighPrev"]
		inpuUp__Prev = owne["inpuUp__Prev"]
		# TODO: a is ""weak"", w is ""weak"". might depend on sensor order
		if A_T.positive:
			inpuRighPrev = -1.0
		if D_T.positive:
			inpuRighPrev = 1.0
		if W_T.positive:
			inpuUp__Prev = 1.0
		if S_T.positive:
			inpuUp__Prev = -1.0
		variDict["inpuRighPrev"] = inpuRighPrev
		variDict["inpuUp__Prev"] = inpuUp__Prev
		if A.positive:
			righ = -1.0
			if inpuRighPrev > 0.0:
				if D.positive:
					righ = 1.0
			magn = 1.0
		elif D.positive:
			righ = 1.0
			magn = 1.0
		if W.positive:
			up__ = 1.0
			if inpuUp__Prev < 0.0:
				if S.positive:
					up__ = -1.0
			magn = 1.0
		elif S.positive:
			up__ = -1.0
			magn = 1.0
	leftShif = owne["leftShif"]
	if keybActi:
		if LEFT_SHIFT.positive:
			leftShif = not leftShif
		if leftShif == False:
			if magn == 1.0:
				magn = 0.7
	else:
		magn = (righ * righ + up__ * up__) ** 0.5
	variDict["leftShif"] = leftShif
	variDict["inpuMagn"] = magn
	variDict["inpuDire"] = math.degrees(math.atan2(up__, righ) - math.pi / 2.0)
	if joys:
		maxi = 2 ** 15 - 1
		thre = owne["joysThre"]
		if joysAxisRigh.positive:
			keybActi = False
			axisRigh = JoysNorm(joysAxisRigh.axisSingle, thre, maxi)
			axisRigh /= bge.render.getWindowWidth()
			# TODO: look up
			axisRigh *= 50.0
			variDict["axisRigh"] = axisRigh
		else:
			variDict["axisRigh"] = 0.0
		if joysAxisUp__.positive:
			keybActi = False
			axisUp__ = JoysNorm(joysAxisUp__.axisSingle, thre, maxi)
			axisUp__ /= bge.render.getWindowWidth()
			# TODO: look up
			axisUp__ *= 50.0
			variDict["axisUp__"] = axisUp__
		else:
			variDict["axisUp__"] = 0.0
	if keyb:
		if keybActi:
			# TODO: call this mous
			if look.positive:
				axisRighPrev = owne["axisRighPrev"]
				difx = bge.logic.mouse.position[0] - axisRighPrev
				sens = owne["lookX___Sens"]
				difx *= sens
				variDict["axisRigh"] = difx
				axisUp__Prev = owne["axisUp__Prev"]
				dify = bge.logic.mouse.position[1] - axisUp__Prev
				# TODO: apply to joystick
				sens = owne["lookY___Sens"]
				dify *= sens
				variDict["axisUp__"] = dify
			# TODO: see if this still works with tuto 5
			mousCentX___ = owne["mousCentX___"]
			mousCentY___ = owne["mousCentY___"]
			if mousCentX___ and mousCentY___:
				bge.logic.mouse.position = (0.5, 0.5)
				variDict["axisRighPrev"] = 0.5
				variDict["axisUp__Prev"] = 0.5
			else:
				if mousCentX___:
					bge.logic.mouse.position = (0.5, bge.logic.mouse.position[1])
					variDict["axisRighPrev"] = 0.5
				else:
					variDict["axisRighPrev"] = bge.logic.mouse.position[0]
				if mousCentY___:
					bge.logic.mouse.position = (bge.logic.mouse.position[0], 0.5)
					variDict["axisUp__Prev"] = 0.5
				else:
					variDict["axisUp__Prev"] = bge.logic.mouse.position[1]
	return variDict

def VariDict(scen, owne):
	retu = {}
	propList = scen.objects[owne].getPropertyNames()
	for prop in propList:
		retu.update({prop : scen.objects[owne][prop]})
	return retu

def Pad_(numb):
	retu = ""
	if numb >= 1000:
		thou = int(numb) / 1000
	if numb < 100:
		retu += "0"
	if numb < 10:
		retu += "0"
	retu += str(numb)
	if numb >= 1000:
		retu = str(thou) + retu
	return retu
