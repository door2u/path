
def main():

	import bge
	import math
	import mathutils
	
	controll = bge.logic.getCurrentController()
	scen = bge.logic.getCurrentScene()
	owne = controll.owner

	import Math
	import game
	import move
	import path
	import cycl
	import look_x
	import look_y
	import orie
	import acti
	import Pyth

	# read properties
	variDict = game.VariDict(scen, owne.name)

	for a in range(variDict["charCoun"]):
		char = variDict["char." + game.Pad_(a)]
		if char:
			charName = scen.name + "." + variDict["charName." + game.Pad_(a)]
			obje = scen.objects[charName]
			variList = obje.getPropertyNames()
			charCont = False
			if "cont" in variList:
				charCont = obje["cont"]
			if charCont:
				# receive input
				variDict = game.Inpu(variDict, owne, owne.sensors['W'], owne.sensors['A'], owne.sensors['S'], owne.sensors['D'], owne.sensors['W_T'], owne.sensors['A_T'], owne.sensors['S_T'], owne.sensors['D_T'], owne.sensors["LEFT_SHIFT"], owne.sensors["RIGHTAXIS"], owne.sensors["UPAXIS"], owne.sensors["joysAxisRigh"], owne.sensors["joysAxisUp__"], owne.sensors["look"], bge, math)
				look = True
				#look = False
				if look:
					# translate mouse movement into angles to apply to camera and object child "look"
					lookX___Angl, lookX___Acti, lookY___Angl, lookY___Acti = Look(charName, "look", "came", variDict, scen, look_x, look_y, math, mathutils)
				else:
					lookX___Angl = 0.0
					lookY___Angl = 0.0
				# get a vector that points in the objects movement direction
				moveVect, upda = move.MoveVect(variDict["inpuDire"], variDict["inpuMagn"], obje.orientation, lookX___Angl, math, Math)
				# get a z angle for the orientation of the object based on movement
				if upda and ("acti" in variList):
					angl = orie.Orie(variDict["inpuDire"], lookX___Angl)
					# apply the orientation
					orientat = MatrEule(scen.objects[obje.name + "." + "body"], mathutils, glob = False)
					scen.objects[obje.name + "." + "body"].orientation = EuleMatr((orientat[0], orientat[1], math.radians(angl)), mathutils)
				if ("acti" in variList):
					# update the cycle animation stage
					actiValu = acti.Acti(obje[obje["acti"]], upda)
					obje[obje["acti"]] = actiValu
			else:
				# call ai functions
				pass
			if upda:
				if ("acti" in variList):
					acti = obje["acti"]
					spee = obje[acti + "Spee"]
				else:
					spee = 0.4
				offs = obje["offs"]
				pathObje = "path"
				# check if the object has left the path and correct its position if necessary
				loca, orientat, pathPolyOffs = path.Path(obje.worldPosition, obje.orientation, obje["pathPolyOffs"], moveVect, variDict["inpuMagn"], spee, offs, False, True, False, False, scen, math, mathutils, Math, pathObje)
				# place the object vertically on the surface of the path
				loca, pathPoly = path.PathGrou(loca, obje["pathPoly"], scen, math, mathutils, Math, pathObje, debu = True)
				obje.worldPosition = loca
				obje.orientation = orientat
				obje["pathPolyOffs"] = pathPolyOffs
				obje["pathPoly"] = pathPoly

			if ("acti" in variList):
				cycl.main(obje, Math)

	# update properties
	# TODO: properties updated by other scripts get reset here
	for key_ in variDict: owne[key_] = variDict[key_]

def Look(charName, lookName, cameName, variDict, scen, look_x, look_y, math, mathutils):
	# x
	orientat = MatrEule(scen.objects[charName + "." + lookName], mathutils, glob = False)
	lookX___Angl, lookX___Acti = look_x.LookX___(scen.objects[charName + "." + lookName], orientat[2], variDict["axisRigh"], math, mathutils)
	scen.objects[charName + "." + lookName].orientation = EuleMatr((orientat[0], orientat[1], math.radians(lookX___Angl)), mathutils)
	# y
	orientat = MatrEule(scen.objects[scen.name + "." + cameName], mathutils, glob = False)
	lookY___Angl, lookY___Acti = look_y.LookY___(scen.objects[scen.name + "." + cameName], orientat[0], variDict["axisUp__"], math, mathutils)
	scen.objects[scen.name + "." + cameName].orientation = EuleMatr((math.radians(lookY___Angl), orientat[1], orientat[2]), mathutils)
	return lookX___Angl, lookX___Acti, lookY___Angl, lookY___Acti

def MatrEule(obje, mathutils, glob = True):
	if glob: orientat = mathutils.Matrix(obje.orientation)
	else: orientat = mathutils.Matrix(obje.localOrientation)
	return orientat.to_euler()

def EuleMatr(eule, mathutils):
	eule = mathutils.Euler(eule, 'XYZ')
	return eule.to_matrix()

main()

