
def Vect(vec1, vec2):
	retu = []
	a = 0
	while a < len(vec1):
		retu.append(vec2[a] - vec1[a])
		a += 1
	return tuple(retu)

def VectDot_(vec1, vec2):
	retu = 0.0
	a = 0
	while a < len(vec1):
		retu += vec1[a] * vec2[a]
		a += 1
	return retu

# is the object in front of the ray
# is a vector facing a point
def Faci(dire, posi, targ):
	retu = True
	vect = Vect(posi, targ)
	dot_ = VectDot_(dire, vect)
	if dot_ < 0.0:
		retu = False
	return retu

def main():

	import bge
	
	cont = bge.logic.getCurrentController()
	scen = bge.logic.getCurrentScene()
	owne = cont.owner

	clic = scen.objects[scen.name + ".scen_obje"]["clic"]

	polyList = []
	coun = scen.objects[scen.name + ".swit.vari"]["swit"]
	for a in range(coun):
		polyList.append(scen.objects[scen.name + ".swit.vari"]["swit." + str(a)])
	#pathPoly = scen.objects[scen.name + "." + "char"]["pathPoly"]
	pathPoly = scen.objects[scen.name + "." + "matt"]["pathPoly"]

	#import math
	#dire = Angl(charName + "." + "body")
	#dire = (math.cos(dire), math.sin(dire))
	#faci = Faci(dire, scen.objects[charName].worldPosition, scen.objects["temp.comp.bool.0.004.in__"].worldPosition)
	#if clic and (pathPoly in polyList) and faci:
	if clic and (pathPoly in polyList):
		owne["active__"] = True
		scen.objects[scen.name + ".swit.on__"].visible = 1
		owne.visible = 0

main()
