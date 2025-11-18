
def PythLink(Pyth = None):
	return Pyth

#################################

# ANGLES

# place an angle in the range (-180.0, 180.0]
def AnglNorm(angl):
	import math
	while angl > 180.0:
		angl -= 360.0
	while angl <= -180.0:
		angl += 360.0
	return angl

# find the difference between two angles
# corrects for problems that might occur if, for example, one angle was 179.0 and the other was -179.0
def AnglDiff(ang1, ang2):
	import math
	return math.fabs(AnglNorm(ang2 - ang1))

# is angle 1 greater than (relatively counter-clockwise to) angle 2
def AnglGrea(ang1, ang2):
	import math
	retu = False
	ang1 -= ang2
	while ang1 > 1.0 * math.pi:
		ang1 -= 2.0 * math.pi
	while ang1 <= -1.0 * math.pi:
		ang1 += 2.0 * math.pi
	if ang1 > 0.0:
		retu = True
	return retu

#################################

# VECTOR FUNCTIONS

def VectDot_(vec1, vec2):
	retu = 0.0
	a = 0
	while a < len(vec1):
		retu += vec1[a] * vec2[a]
		a += 1
	return retu

def VectMagn(vect):
	return VectDot_(vect, vect) ** 0.5

def Vect(vec1, vec2):
	retu = []
	a = 0
	while a < len(vec1):
		retu.append(vec2[a] - vec1[a])
		a += 1
	return tuple(retu)

def VectAdd_(vec1, vec2):
	retu = []
	a = 0
	while a < len(vec1):
		retu.append(vec1[a] + vec2[a])
		a += 1
	return tuple(retu)

def VectScal(vect, scal):
	retu = []
	a = 0
	while a < len(vect):
		retu.append(vect[a] * scal)
		a += 1
	return tuple(retu)

def VectNorm(vect):
	import math
	tole = 0.0001
	magn = VectMagn(vect)
	retu = []
	a = 0
	while a < len(vect):
		if math.fabs(magn) >= tole:
			retu.append(vect[a] / magn)
		else:
			retu.append(0.0)
		a += 1
	return tuple(retu)

def Dist(vec1, vec2):
	return VectMagn(Vect(vec1, vec2))

def VectCros3d__(vec1, vec2):
	a = vec1[1] * vec2[2] - vec1[2] * vec2[1]
	b = vec1[0] * vec2[2] - vec1[2] * vec2[0]
	c = vec1[0] * vec2[1] - vec1[1] * vec2[0]
	return (a, -b, c)

def VectAngl(vec1, vec2, tole = 0.0001, prin = False):
	import math
	retu = 0.0
	deno = VectMagn(vec1) * VectMagn(vec2)
	if math.fabs(deno) >= tole:
		argu = VectDot_(vec1, vec2) / deno
		if math.fabs(argu) <= 1.0 + tole:
			if argu > 1.0:
				argu = 1.0
			if argu < -1.0:
				# TODO: error?
				#argu = 1.0
				argu = -1.0
			# TODO: returning degrees
			retu = math.degrees(math.acos(argu))
		else:
			if prin == True:
				print("math domain error", argu)
	else:
		if prin == True:
			print("approaching divide by 0", deno)
	return retu

# project vec1 onto vec2
def VectProj(vec1, vec2):
	import math
	tole = 0.0001
	# TODO
	retu = "divide by 0 error"
	deno = VectDot_(vec2, vec2)
	if math.fabs(deno) >= tole:
		nume = VectDot_(vec1, vec2)
		nume /= deno
		nume = VectScal(vec2, nume)
		retu = nume
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

# TODO: is this supposed to always return a positive result?
# distance from a point to the nearest point on an infinite plane. planPoin can be any point as long as it lies on the surface of the plane (like the face center)
def DistPoinPlan(poin, planPoin, norm):
	import math
	tole = 0.0001
	deno = VectDot_(norm, norm)
	dist = 0.0
	chec = False
	if math.fabs(deno) >= tole:
		vect = Vect(planPoin, poin)
		vect = VectProj(vect, norm)
		dist = VectMagn(vect)
		chec = True
	# TODO
	if chec == False:
		dist = "divide by zero error"
	return dist

# get the distance to the point where a vector intersects a plane
# assumes vectDire and norm are normalized
def DistVectPlan(vectOrig, vectDire, poin, norm, tole = 0.0001):
	import math
	# normal is the direction of the plane
	deno = VectDot_(vectDire, norm)
	# TODO
	dist = "divide by zero error"
	if math.fabs(deno) > tole:
		# point is any point on the plane being checked for distance to ray origin. it could be the face center for the polygon, for example.
		vect = Vect(vectOrig, poin)
		dist = VectDot_(vect, norm) / deno
	return dist

def PlanAngl(loca, fro_, norm, dot_, vert, dire):
	angl = -1
	vectOrig = VectAdd_(loca, fro_)
	dist = DistVectPlan(vectOrig, dire, vert, norm)
	if type(dist) == float:
		poin = VectScal(dire, dist)
		poin = VectAdd_(poin, vectOrig)
		vect = Vect(loca, poin)
		angl = VectAngl(vect, fro_)
		cros = VectCros3d__(vect, fro_)
		if VectDot_(cros, dot_) >= 0.0:
			angl *= -1.0
	return angl

# TODO: 3d
# get the distance along 2d vec1 that meets with vec2
def VectInte2d__(ori1, vec1, ori2, vec2, tole = 0.0001):
	return DistVectPlan(ori1, VectNorm(vec1), ori2, VectNorm((-vec2[1], vec2[0])), tole = tole)

def VectSame(vec1, vec2, tole = 0.0001):
	import math
	retu = True
	a = 0
	while a < len(vec1):
		if math.fabs(vec1[a] - vec2[a]) > tole:
			retu = False
		a += 1
	return retu

def VectInve(vect):
	return tuple(VectScal(vect, -1.0))

# convert a vector to an euler rotation
# assumes object was originally oriented towards +x
# TODO: too many cases
def VectTo__Eule3d__(vect):
	import math
	tole = 0.0001
	x = 0.0
	z = math.atan2(vect[1], vect[0])
	if math.fabs(vect[0]) >= tole:
		z2 = math.cos(z)
		if math.fabs(z2) >= tole:
			x2 = vect[0] / z2
		else:
			x2 = vect[0]
		y = math.atan2(-vect[2], x2)
	else:
		# TODO: when did this get messed up
		#if math.fabs(vect[1]) >= 0.0:
		if vect[1] > 0.0:
			y = math.atan2(-vect[2], vect[1])
		else:
			y = math.atan2(-vect[2], -vect[1])
	return VectDegr((x, y, z))

def EuleTo__Matr3d__Axis(rota):
	import math
	rota = (math.degrees(rota[0]), math.degrees(rota[1]), math.degrees(rota[2]))
	forw = EuleTo__Vect3d__(rota, vect = (1.0, 0.0, 0.0))
	othe = EuleTo__Vect3d__(rota, vect = (0.0, 1.0, 0.0))
	z___ = EuleTo__Vect3d__(rota, vect = (0.0, 0.0, 1.0))
	return forw, othe, z___

def EuleTo__Vect3d__(eule, vect = (1.0, 0.0, 0.0)):
	vect = Quat(vect, eule[0], (1.0, 0.0, 0.0))
	vect = Quat(vect, eule[1], (0.0, 1.0, 0.0))
	vect = Quat(vect, eule[2], (0.0, 0.0, 1.0))
	return vect

# TODO: description
# simple case where y rotation is 0.0
def VectRotaSimp(vect, rotx, rotz):
	import math
	z = vect[1] * math.sin(rotx) + vect[2] * math.cos(rotx)
	y = vect[1] * math.cos(rotx) - vect[2] * math.sin(rotx)
	vect = (vect[0], y, vect[2])
	y = vect[0] * math.sin(rotz) + vect[1] * math.cos(rotz)		
	x = vect[0] * math.cos(rotz) - vect[1] * math.sin(rotz)
	return (x, y, z)

# vector psuedo rotate
# change the direction of a vector according to the endpoint of a different vector
# this can be used to make passable physics animations where computational efficiency is preferred over accuracy
def VectPsueRota(vec1, vec2):
	import math
	magn = VectMagn(vec1)
	retu = VectNorm(VectAdd_(vec1, vec2))
	retu = VectScal(retu, magn)
	return retu

# return a vector orthogonal to u that lies in the plane of vectors U and V
def ProjOrth(u, v):
	# project v onto u
	u = VectProj(v, u)
	u = VectInve(u)
	return VectAdd_(v, u)

#################################

# VECTOR LISTS

# make a list of vectors to a given point
def VectList(give, vectList):
	retu = []
	a = 0
	while a < len(vectList):
		retu.append(Vect(give, vectList[a]))
		a += 1
	return retu

# get the magnitudes of a list of vectors
def VectMagnList(vectList):
	retu = []
	a = 0
	while a < len(vectList):
		retu.append(VectMagn(vectList[a]))
		a += 1
	return retu

# get the angles of a list of vectors
def VectAnglList(give, vectList):
	retu = []
	a = 0
	while a < len(vectList):
		retu.append(VectAngl(give, vectList[a]))
		a += 1
	return retu

# get the closest point to a list of vectors
def VectClos(give, vectList, excl = []):
	vectList = VectList(give, vectList)
	vectList = VectMagnList(vectList)
	clos, dist = Clos(0.0, vectList, excl = excl)
	return clos, dist

# find the smallest vector angle in a list to a given vector
def VectClosAngl(give, vectList, tole = 0.0001):
	list = VectList(give, vectList)
	list = VectAnglList(give, vectList)
	clos, dist = Clos(0.0, vectList)
	return clos, dist

# find the closest float to a given from a list
def Clos(give, list, excl = []):
	import math
	distClos = -1.0
	clos = -1
	a = 0
	while a < len(list):
		exc_ = False
		for b in range(len(excl)):
			if a == excl[b]:
				exc_ = True
				break
		if exc_ == False:
			dist = math.fabs(give - list[a])
			if distClos >= 0.0:
				if dist < distClos:
					distClos = dist
					clos = a
			else:
				distClos = dist
				clos = a
		a += 1
	return clos, distClos

# return the average vector in a list of vectors (to get the average location of a group of objects, as in CursTo__Sele(all_ = True), for example)
def VectAver(vectList):
	retu = None
	if len(vectList) > 0:
		retu = list(vectList[0])
		for a in range(len(retu)):
			retu[a] = 0.0
	a = 0
	for vect in vectList:
		for b in range(len(vect)):
			retu[b] += vect[b]
		a += 1
	if a != 0:
		retu = VectScal(retu, 1.0 / a)
	#if a != 0:
	#	for b in range(len(retu)):
	#		retu[b] /= a - 0
		retu = tuple(retu)
	return retu

# convert a list or tuple of radian angles to a tuple of degree angles
def VectDegr(vect):
	import math
	retu = []
	a = 0
	while a < len(vect):
		retu.append(math.degrees(vect[a]))
		a += 1
	return tuple(retu)

# convert a list or tuple of degree angles to a tuple of radian angles
def VectRadi(vect):
	import math
	retu = []
	a = 0
	while a < len(vect):
		retu.append(math.radians(vect[a]))
		a += 1
	return tuple(retu)

#################################

# MATRICES

# copy rows to columns
def MatrDeco(matr):
	retu = []
	leng = -1
	if len(matr) > 0:
		leng = len(matr[0])
	for a in range(leng):
		row_ = []
		for b in range(len(matr)):
			row_.append(matr[b][a])
		retu.append(row_)
	return retu

def Matr(mat1 = [], mat2 = [], deco = True):
	retu = []
	leng = -1
	if len(mat1) > 0:
		leng = len(mat1[0])
	# check if the column count of the first matrix matches the row count of the second matrix
	if len(mat2) == leng:
		if deco == True:
			mat2 = MatrDeco(mat2)
		for a in range(len(mat1)):
			row_ = []
			for b in range(len(mat2)):
				vec1 = mat1[a]
				vec2 = mat2[b]
				row_.append(VectDot_(vec1, vec2))
			retu.append(row_)
	else:
		print("matrix sizes do not match")
	return retu

#################################

# TRANSFORMS

# rotate a 2 dimensional vector
def VectRota2d__(vect, rota, axis):
	import math
	if axis == None:
		axis = 0
	mat1 = []
	if axis == 0 or axis == 2:
		mat1.append([math.cos(math.radians(rota)), -math.sin(math.radians(rota))])
		mat1.append([math.sin(math.radians(rota)), math.cos(math.radians(rota))])
	if axis == 1:
		mat1.append([math.cos(math.radians(rota)), math.sin(math.radians(rota))])
		mat1.append([-math.sin(math.radians(rota)), math.cos(math.radians(rota))])
	mat2 = []
	mat2.append([vect[0]])
	mat2.append([vect[1]])
	retu = Matr(mat1, mat2)
	return retu

# rotate a 3d vector
def VectRota3d__(vect, eule):
	vecx = VectRota2d__((vect[1], vect[2]), eule[0], 0) # y z
	vecy = VectRota2d__((vect[0], vecx[1][0]), eule[1], 1) # x z
	vecz = VectRota2d__((vecy[0][0], vecx[0][0]), eule[2], 2) # x y
	return (vecz[0][0], vecz[1][0], vecy[1][0])

# rotate poin angl degrees around axis
# 3d point
# angle in degrees
# normalized axis
def Quat(poin, angl, axis):
	import math
	p = poin[0]
	q = poin[1]
	r = poin[2]
	t = math.radians(angl)
	t /= 2.0
	a = math.cos(t)
	b = math.sin(t)
	x = axis[0]
	y = axis[1]
	z = axis[2]
	#o = -a*b*p*x-a*b*q*y-a*b*r*z-b*b*p*y*z-b*b*q*x*z-b*b*r*x*y+a*b*p*x+a*b*q*y+a*b*r*z+b*b*p*y*z+b*b*q*x*z+b*b*r*x*y
	#i = -a*b*q*z-a*b*q*z-b*b*p*y*y-b*b*p*z*z+a*a*p+a*b*r*y+a*b*r*y+b*b*p*x*x+b*b*q*x*y+b*b*q*x*y+b*b*r*x*z+b*b*r*x*z
	#j = -a*b*r*x-a*b*r*x-b*b*q*x*x-b*b*q*z*z+a*a*q+a*b*p*z+a*b*p*z+b*b*p*x*y+b*b*p*x*y+b*b*q*y*y+b*b*r*y*z+b*b*r*y*z
	#k = -a*b*p*y-a*b*p*y-b*b*r*x*x-b*b*r*y*y+a*a*r+a*b*q*x+a*b*q*x+b*b*p*x*z+b*b*p*x*z+b*b*q*y*z+b*b*q*y*z+b*b*r*z*z
	i = r*(2*b*b*x*z+2*a*b*y)+b*b*p*x*x+2*b*b*q*x*y-b*b*p*y*y-b*b*p*z*z-2*a*b*q*z+a*a*p
	j = r*(2*b*b*y*z-2*a*b*x)-b*b*q*x*x+2*b*b*p*x*y+b*b*q*y*y-b*b*q*z*z+2*a*b*p*z+a*a*q
	k = r*(-b*b*x*x-b*b*y*y+b*b*z*z+a*a)+x*(2*b*b*p*z+2*a*b*q)+y*(2*b*b*q*z-2*a*b*p)
	return (i, j, k)

# TODO: maybe ScalAppl or something
def EngiScal(vect, scal):
	retu = []
	a = 0
	while a < len(vect):
		retu.append(vect[a] * scal[a])
		a += 1
	return tuple(retu)

# apply the transformation of a 3d point
def Tran3d__(vect, scal, rota, loca):
	import math
	vect = EngiScal(vect, scal)
	# TODO: which is faster
	vect = VectRota3d__(vect, rota)
	#vect = Quat(vect, math.degrees(rota[0]), (1.0, 0.0, 0.0))
	#vect = Quat(vect, math.degrees(rota[1]), (0.0, 1.0, 0.0))
	#vect = Quat(vect, math.degrees(rota[2]), (0.0, 0.0, 1.0))
	vect = VectAdd_(vect, loca)
	return vect

def TranList(vectList, scal, rota, loca):
	retu = []
	a = 0
	while a < len(vectList):
		retu.append(Tran3d__(vectList[a], scal, rota, loca))
		a += 1
	return retu

#################################

# RANDOM

def Rand(maxi):
	import random
	random.seed()
	return random.random() * maxi - maxi / 2.0

def RandRang(mini, maxi):
	import random
	random.seed()
	rand = random.random() * (maxi - mini)
	return mini + rand

# randomly offset a vert list
def VertListRand(vert = [], maxi = 1.0):
	a = 0
	while a < len(vert):
		vert[a] = VectAdd_(vert[a], VertRand(maxi))
		a += 1
	return vert

def VertRand(maxi = 1.0):
	ranx = Rand(maxi)
	rany = Rand(maxi)
	ranz = Rand(maxi)
	return (ranx, rany, ranz)

# TODO: [1 / root(2pi)] * e ^ (-x^2) / 2

#################################

# GEOMETRY

# connect vertices in a series
def EdgeLine(size):
	edgeList = []
	a = 0
	while a < size:
		edgeList.append((a, a + 1))
		a += 1
	return edgeList

# create a list of vertex normals from a polygon list and normal list
def VertNorm(leng, polyList, normList):
	vertNorm = []
	tole = 0.001
	for a in range(leng):
		nor_List = []
		for b in range(len(polyList)):
			ver1 = polyList[b][0]
			ver2 = polyList[b][1]
			ver3 = polyList[b][2]
			if a == ver1 or a == ver2 or a == ver3:
				exis = False
				for c in range(len(nor_List)):
					if VectDot_(nor_List[c], normList[b]) > 1.0 - tole:
						exis = True
						break
				if exis == False:
					nor_List.append(normList[b])
		norm = VectAver(nor_List)
		norm = VectNorm(norm)
		vertNorm.append(norm)
	return vertNorm

def Elli(t = 0.0, spee = 1.0, radi = 0.2, phas = 0.0, rati = 0.2):
	import math
	y = radi * math.sin(t * 2.0 * math.pi * spee + phas)
	x = radi * math.cos(t * 2.0 * math.pi * spee + phas)
	y *= rati
	return x, y

# TODO
# merge a/b loops
# calculate top and merge poly / vert loops
# define vertex indices
def Sphe(segs = 32, ring = 16, cent = (0.0, 0.0, 0.0), radi = 1.0, distCirc = True):
	import math
	vert = []
	edge = []
	poly = []
	# bottom
	vert.append(VectAdd_(cent, (0.0, 0.0, -radi)))
	z = radi
	radiAdju = radi
	for a in range(0, int(segs / 2) + 1):
		for b in range(1, ring):
			if distCirc == True:
				z = radi * math.cos((b * math.pi) / ring)
				radiAdju = radi * math.sin((b * math.pi) / ring)
			else:
				z = -2.0 * radi * b / ring + radi
				radiAdju = (radi * radi - z * z) ** 0.5
			x = radiAdju * math.cos((-(a + 1) * 2.0 * math.pi) / segs + math.pi / 2.0)
			y = radiAdju * math.sin((-(a + 1) * 2.0 * math.pi) / segs + math.pi / 2.0)
			vert.append(VectAdd_(cent, (x, y, z)))
			if a == 0:
				if b < ring - 1:
					# connect first segment
					edge.append((b, b + 1))
			else:
				# connect segment
				if b < ring - 1:
					edge.append((b + (a * ring) - a, b + (a * ring) - a + 1))
				# connect ring
				edge.append((b + ((a - 1) * ring) - a + 1, b + (a * ring) - a))
	# top
	vert.append(VectAdd_(cent, (0.0, 0.0, radi)))
	top_ = len(vert) - 1
	# top to top of middle segment
	edge.append((top_, 1 + ((int(segs / 2) + 1) * ring) - (int(segs / 2) + 1) + 1))
	c = 0
	d = 1
	for a in range(int(segs / 2) + 1, segs):
		for b in range(1, ring):
			if distCirc == True:
				z = radi * math.cos((b * math.pi) / ring)
				radiAdju = radi * math.sin((b * math.pi) / ring)
			else:
				z = -2.0 * radi * b / ring + radi
				radiAdju = (radi * radi - z * z) ** 0.5
			x = radiAdju * math.cos((-(a + 1) * 2.0 * math.pi) / segs + math.pi / 2.0)
			y = radiAdju * math.sin((-(a + 1) * 2.0 * math.pi) / segs + math.pi / 2.0)
			vert.append(VectAdd_(cent, (x, y, z)))
			# connect segment
			if b < ring - 1:
				edge.append((b + (a * ring) - a + 1, b + (a * ring) - a + 2))
			# connect ring
			edge.append((b + ((a - 1) * ring) - a + d, b + (a * ring) - a + c + d))
		if c == 0:
			c = -1
		if d == 1:
			d = 2
		# top / bottom of last segment
		if a == segs - 1:
			edge.append((top_, 1 + (a * ring) - a + 1))
			edge.append((ring - 2 + (a * ring) - a + 2, 0))
	###########################
	# top / bottom of first segment
	edge.append((top_, 1))
	edge.append((ring - 1, 0))
	# final ring (last to first)
	for b in range(1, ring):
		edge.append((b, b + ((segs - 1) * ring) - (segs - 1) + 1))
	# top / bottom of first half
	for a in range(1, int(segs / 2) + 1):
		edge.append((top_, 1 + (a * ring) - a + 0))
		edge.append((ring - 2 + (a * ring) - a + 1, 0))
	# top / bottom of second half
	for a in range(int(segs / 2) + 1, segs):
		if a != int(segs / 2) + 1:
			edge.append((top_, 1 + (a * ring) - a + 1))
		edge.append((ring - 2 + (a * ring) - a + 2, 0))
	###########################
	# ending to starting segment
	for b in range(1, ring - 1):
		poly.append((b + 1, b + ((segs - 1) * ring) - (segs - 1) + 2, b + ((segs - 1) * ring) - (segs - 1) + 1, b))
	# top
	poly.append((1, 1 + ((segs - 1) * ring) - (segs - 1) + 1, top_))
	# bottom
	poly.append((0, ring - 1 + ((segs - 1) * ring) - (segs - 1) + 1, ring - 1))	
	# first half of segments
	for a in range(1, int(segs / 2) + 1):
		for b in range(1, ring - 1):
			poly.append((b + ((a - 1) * ring) - (a - 1), b + (a * ring) - a, b + (a * ring) - a + 1, b + ((a - 1) * ring) - (a - 1) + 1))
		poly.append((1 + (a * ring) - a, 1 + ((a - 1) * ring) - (a - 1), top_))
		poly.append((0, ring - 1 + ((a - 1) * ring) - (a - 1), ring - 1 + (a * ring) - a))
	# second half of segments
	c = 0
	d = 1
	for a in range(int(segs / 2) + 1, segs):
		for b in range(1, ring - 1):
			poly.append((b + ((a - 1) * ring) - a + d + 1, b + ((a - 1) * ring) - a + d, b + (a * ring) - a + c + d, b + (a * ring) - a + c + d + 1))
		poly.append((1 + (a * ring) - a + c + d, 1 + ((a - 1) * ring) - a + d, top_))
		poly.append((0, ring - 1 + ((a - 1) * ring) - a + d, ring - 1 + (a * ring) - a + c + d))
		if c == 0:
			c = -1
		if d == 1:
			d = 2
	return vert, edge, poly

#################################

# SIMPLIFICATION

# form a list of expressions from a string
def ExprPars(expr):
	Pyth = PythLink()
	expr = Pyth.Whit(expr)
	variList = [expr]
	brea = False
	while brea == False:
		brea = True
		for a in range(len(variList)):
			variList, appe = ExprSepaEncl(a, variList)
			if appe == True:
				brea = False
	#print(variList)
	operList = ["^", "*", "+"]
	for oper in operList:
		brea = False
		while brea == False:
			brea = True
			for a in range(len(variList)):
				#print(a, variList)
				variList, appe = ExprSepaVari(a, variList, oper = oper)
				#if oper == "+":
				#	print(a)
				if appe == True:
					brea = False
	#print("here")
	print(variList)
	quit()
	for oper in operList:
		brea = False
		while brea == False:
			brea = True
			for a in range(len(variList)):
				variList, appe = ExprSepaOper(a, variList, oper = oper)
				if appe == True:
					brea = False
	print(variList)
	return variList


def ExprSepaEncl(inde, variList):
	encl = Encl(variList[inde])
	# was a change to the list made
	appe = False
	while encl != None:
		appe = True
		variList[inde] = variList[inde].replace("(" + encl + ")", "@" + str(len(variList)), 1)
		variList.append(encl)
		encl = Encl(variList[inde])
	return variList, appe

def Encl(stri):
	retu = ""
	pareCoun = 0
	pareStar = False
	star = 0
	a = 0
	while a < len(stri):
		if stri[a] == ")":
			if pareCoun > 0:
				pareCoun -= 1
		if pareStar == True:
			if pareCoun == 0:
				retu = stri[star + 1:a]
				pareStar = False
				break
		if stri[a] == "(":
			pareCoun += 1
			if pareStar == False:
				star = a
			pareStar = True
		a += 1
	if a == len(stri):
		retu = None
	return retu

def ExprSepaVari(inde, variList, oper = "^"):
	#print("vli", variList[inde])
	variStri = Vari(variList[inde], oper = oper)
	#print("v", variStri)
	# was a change to the list made
	appe = False
	a = 0
	while variStri != None:
		appe = True
		#print(variList[inde], variList, variStri)
		#print("b", variList[inde], variStri)

		repl = "@"
		#if variStri[0] == "/":
		#	repl = "*@"
		#	variStri = "*" + variStri
		#if variStri[0] == "-":
		#	repl = "+@"
		#	variStri = "+" + variStri
		
		variList[inde] = ReplExpr(variList[inde], repl + str(len(variList)), variStri)
		#print(variList[inde], repl + str(len(variList)), variStri, inde)
		#print("a", variList[inde])
		
		variList.append(variStri)
		variStri = Vari(variList[inde], oper = oper)

		#print("vl", variList)
		#quit()

		a += 1
	return variList, appe

def Vari(expr, oper = "^"):
	retu = ""
	operFlag = False
	#if oper == "+":
	#	print("e", expr)
	#	quit()
	#if expr == "3.5+5.5":
	#	print("3.5+5.5")
	#	quit()
	#	#expr="3+5"
	print(expr)
	a = 0
	while a < len(expr):
		#if expr[a].isnumeric():
		if expr[a].isnumeric() or expr[a] == ".":
			inde = False
			b = a
			while b >= 0:
				if expr[b] == "@":
					inde = True
					break
				if expr[b].isnumeric() == False:
					break
				b -= 1
			if inde == False:
				retu += expr[a]
		if expr[a] == "/" or expr[a] == "-" or expr[a].isalpha():
			retu += expr[a]
		# TODO: what happens if expr[a] ==  oper is used instead of operis__
		nega = False
		if (oper == "*" and expr[a] == "/") or (oper == "+" and expr[a] == "-"):
			nega = True
		#if OperIs__(expr[a]) or a == len(expr) - 1:
		if OperIs__(expr[a]) or nega or a == len(expr) - 1:
			#if expr[a] == oper:
			if expr[a] == oper or nega:
				#print("here")
				operFlag = True
			#if operFlag and retu != "":
			if operFlag and retu != "" and retu != "/" and retu != "-":
				break
		#print(a)
		a += 1
	if a == len(expr):
		retu = None

	#if expr == "3.5+5.5":
	#	#print("3.5+5.5")
	#	print("retu", retu)
	#	quit()

	print(retu)

	return retu

def ExprSepaOper(inde, variList, oper = "^"):
	sepa = Oper(variList[inde], oper = oper)
	# was a change to the list made
	appe = False
	while sepa != None:
		appe = True
		variList[inde] = ReplExpr(variList[inde], "@" + str(len(variList)), sepa)
		variList.append(sepa)
		sepa = Oper(variList[inde], oper = oper)
	return variList, appe

# TODO: this might be the same as split(oper), retu[1] = retu[1:len(retu)] or something
# expr: str. oper: "^", "*", "+"
def Oper(expr = "", oper = "^"):
	stri = ""
	# return a list of length 2 for each string separated by oper
	retu = []
	# index 
	inde = -1
	a = 0
	while a < len(expr):
		#if expr[a] == oper or (oper == "*" and expr[a] == "/") or (oper == "+" and expr[a] == "-"):
		#if expr[a] == oper:
		if OperIs__(expr[a]):
			retu.append(stri)
			if inde != -1 and len(retu) > 2:
				break
			stri = ""
			#if expr[a] != oper:
			#	stri += expr[a]
			# TODO: whats the difference
			#if inde == -1:
			if inde == -1 and expr[a] == oper:
				inde = len(retu)
		else:
			stri += expr[a]
		a += 1
	if a == len(expr) and stri != "":
	#if a == len(expr) and stri != "" and stri != "/" and stri != "-":
		retu.append(stri)
	#print(inde, retu)
	# TODO:
	if inde != -1 and len(retu) > 2:
		retu = retu[inde - 1] + oper + retu[inde]

		

	else:
		retu = None

	print("retu", retu)

	return retu

# replace something thats not already an index
def ReplExpr(stri, repl, find):

	#st = "asdf"
	#fi = "sd"
	#i = st.find(fi)
	#print(st[i])

	print("srf", stri, repl, find)
	#find = "2"
	strc = stri
	shif = 0
	brea = False
	while True:
		inde = strc.find(find)
		print("inde", inde)
		#print("sci", strc[inde])
		if inde == -1:
			break
		indc = inde
		while indc >= 0:
			# TODO?
			#indc -= 1
			if strc[indc] == "@":
				break
			if strc[indc].isalnum() == False:
			#if strc[indc].isalnum() == False and strc[indc] != "/" and strc[indc] != "-":
				brea = True
				
				break
			indc -= 1
		print("indc", indc)
		if brea == True:
			break
		if indc == -1:
			break
		while strc[inde].isnumeric():
		#while inde < len(strc) and (strc[inde].isnumeric() or strc[inde] == "/" or strc[inde] == "-"):
			#if inde < len(strc):
			#	print(inde, strc[inde])
			inde += 1
		print(inde, strc[inde])
		strc = strc[inde + 1:len(strc)]
		print("c", strc)
		shif += inde + 1
	if inde != -1:
		if inde != 0 and repl[0] == '@':
			#print("here")
			#quit()
			if find[0] == '/':
				repl = "*" + repl
			if find[0] == '-':
				repl = "+" + repl
		inde += shif
		strc = ""
		a = 0
		while a < inde + 0:
			strc += stri[a]
			a += 1
		strc += repl
		a += len(find)
		while a < len(stri):
			strc += stri[a]
			a += 1
	else:
		strc = stri
	print("retu", strc)
	return strc

###

def OperType(entr):
	retu = ""
	for a in range(len(entr)):
		if OperIs__(entr[a]):
			retu = entr[a]
			break
	return retu

def OperIs__(char):
	return char == "^" or char == "*" or char == "+"

def IndeHas_(expr):
	retu = False
	for a in range(len(expr)):
		if expr[a] == "@":
			retu = True
			break
	return retu

###

#################################

# SOLVING

def Pop_(list, pop_List):
	# sort
	pop_List = sorted(pop_List)
	# purge duplicates
	a = len(pop_List) - 1
	while a >= 1:
		b = a - 1
		while b >= 0:
			if pop_List[a] == pop_List[b]:
				pop_List.pop(a)
				break
			b -= 1
		a -= 1
	# pop
	a = len(pop_List) - 1
	while a >= 0:
		list.pop(pop_List[a])
		a -= 1
	return list
	

def FactStri(inte):
	return "!" + str(int(inte))

# func: 0 for sine, 1 for cosine, 2 for arctangent
# atan:
# x - x**3/3 + x**5/5 - x**7/7 + x**9/9 + ...
def SineTerm(coun = 6, func = 0, vari = "x"):
	retu = Equa()
	subt = False
	for a in range(coun):
		inte = int(2.0 * a)
		if func == 0 or func == 2:
			inte += 1
		fact = FactStri(inte)
		if func == 2:
			fact = inte
		term = Term([vari, fact])
		term.expo[len(term.expo) - 2] *= inte
		term.expo[len(term.expo) - 1] = -1
		if subt == True:
			term.valu *= -1.0
		subt = not subt
		retu.Appe(term)
	return retu

"""
def AtanTerm(coun = 6, vari = "x"):
	retu = Equa()
	subt = False
	for a in range(coun):
		inte = int(2.0 * a)
		#if cosi == False:
		inte += 1
		#fact = FactStri(inte)
		term = Term([vari, inte])
		term.expo[len(term.expo) - 2] *= inte
		term.expo[len(term.expo) - 1] = -1
		if subt == True:
			term.valu *= -1.0
		subt = not subt
		retu.Appe(term)
	return retu
"""

# TODO: name conflict
"""
class Vari(list):
	def __init__(self, pare, vari = None):
		self.pare = pare
		if type(vari) == str:
			self.Appe(vari)
		elif type(vari) == list:
			for item in vari:
				self.Appe(item)
	def Appe(self, appe):
		if (type(appe) == str and len(appe) > 0) or type(appe) == float or type(appe) == int:
			if len(self) == 0 and self.pare.valu == 0.0:
				self.pare.valu = 1.0
			expo = self.pare.expo
			#expo.insert(len(self)
			expo.append(1)
			if type(appe) == str:
				if appe[0] == "-":
					self.pare.valu *= -1.0
					appe = appe[1:len(appe)]
			orde = len(self)
			#self.insert
			self.append([appe, orde])
	def Inse(self, inde, appe, expoInse = True):
		if (type(appe) == str and len(appe) > 0) or type(appe) == float or type(appe) == int:
			if expoInse == True:
				expo = self.pare.expo
				expo.insert(inde, 1)
			if type(appe) == str:
				if appe[0] == "-":
					self.pare.valu *= -1.0
					appe = appe[1:len(appe)]
			#orde = inde
			self.insert(inde, [appe, inde])
			#self.append()

	def Sort(self):
		a = 0
		while a < len(self) - 1:
			if type(self[a][0]) == str and len(self[a][0]) > 0:
				com1 = ""
				com2 = ""
				if type(self[a][0]) == str:
					com1 = self[a][0][0]
				# TODO: is this a typo?
				#if type(self[a][0]) == str:
				if type(self[a + 1][0]) == str:
					com2 = self[a + 1][0][0]
				typ_ = False
				if type(self[a][0]) == type(self[a + 1][0]):
					typ_ = True
				matc = False
				if (com1 != "!" and com2 != "!") or (com1 == "!" and com2 == "!"):
					matc = True
				unor = False
				if typ_ and self[a + 1][0] < self[a][0]:
					unor = True
				if (matc and unor) or (com1 == "!" and com2 != "!"):
					temp = self[a]
					self[a] = self[a + 1]
					self[a + 1] = temp
					a = -1
			a += 1
		return self
"""

class Term:

	def __init__(self, vari = None):
		self.valu = 0.0
		if type(vari) == float or type(vari) == int:
			self.valu = vari
		elif type(vari) == str:
			self.valu = 1.0
		self.expo = []
		self.vari = Vari(self, vari)

	def __add__(self, othe):
		retu = Equa(self)
		retu.Appe(othe)
		retu.Clea()
		return retu
	def __iadd__(self, othe):
		retu = Equa(self)
		retu.Appe(othe)
		retu.Clea()
		return retu

	def __sub__(self, othe):
		if type(othe) == Term:
			othe.valu *= -1.0
		elif type(othe) == Equa:
			for a in range(len(othe)):
				othe[a].valu *= -1.0
		retu = Equa(self)
		retu.Appe(othe)
		retu.Clea()
		return retu
	def __isub__(self, othe):
		if type(othe) == Term:
			othe.valu *= -1.0
		elif type(othe) == Equa:
			for a in range(len(othe)):
				othe[a].valu *= -1.0
		retu = Equa(self)
		retu.Appe(othe)
		retu.Clea()
		return retu

	#a * b

	def TermMult(self, term):
		retu = self.Copy()
		leng = len(retu.vari)
		for a in range(len(term.vari)):
			retu.vari.Appe(term.vari[a][0])
			retu.expo[leng + a] = term.expo[a]
		retu.Sort()
		retu.Orde()
		retu.valu = self.valu * term.valu
		return retu

	def __mul__(self, othe):
		if type(othe) == Term:
			retu = self.TermMult(othe)
			retu = Equa(retu)
		elif type(othe) == Equa:
			retu = othe.Copy()
			retu *= self
		retu.Clea()
		return retu

	# *=
	def __imul__(self, othe):
		if type(othe) == Term:
			retu = self.TermMult(othe)
			retu = Equa(retu)
		elif type(othe) == Equa:
			retu = othe.Copy()
			retu *= self
		retu.Clea()
		return retu

	

	def Clea(self):
		self.Sort()
		self.Simp()
		self.Orde()

	def Sort(self):
		self.vari.Sort()
		self.SortExpo()

	def SortExpo(self):
		expo = []
		for a in range(len(self.vari)):
			expo.append(self.expo[self.vari[a][1]])
		self.expo = expo[:]

	def Simp(self):
		self.SimpExpo()
		self.SimpVari()
		self.SimpFact()
		self.SimpFloa()

	def SimpExpo(self):
		for a in range(len(self.vari)):
			if self.expo[a] == 0:
				self.vari[a][0] = 1
				self.expo[a] = 1
		return self

	# ie a^1*a^1 -> a^2
	def SimpVari(self):
		pop_List = []
		for a in range(len(self.vari) - 1):
			for b in range(a + 1, len(self.vari)):
				#if self.var[a][0] == self.vari[b][0]:
				if self.vari[a][0] == self.vari[b][0]:
					self.expo[a] += self.expo[b]
					pop_List.append(b)
		self.Pop_(pop_List)
		return self

	def SimpFact(self):
		for a in range(len(self.vari)):
			if type(self.vari[a][0]) == str and len(self.vari[a][0]) > 1:
				if self.vari[a][0][0] == "!":
					if len(self.vari[a][0]) == 2 and (self.vari[a][0][1] == "0" or self.vari[a][0][1] == "1"):
						self.vari[a][0] = 1.0
					elif len(self.vari[a][0]) == 2 and self.vari[a][0][1] == "2":
						self.vari[a][0] = 2.0
					else:
						valu = 1.0
						fact = self.vari[a][0][1:len(self.vari[a][0])]
						fact = int(fact)
						if fact > 1:
							for b in range(2, fact + 1):
								valu *= b
						self.vari[a][0] = valu
		return self

	def SimpFloa(self):
		pop_List = []
		for a in range(len(self.vari)):
			valu = self.vari[a][0]
			if type(valu) == float or type(valu) == int:
				valu = valu ** self.expo[a]
				self.valu *= valu
				pop_List.append(a)
		self.Pop_(pop_List)
		return self

	def Pop_(self, pop_List):
		self.vari = Pop_(self.vari, pop_List)
		self.expo = Pop_(self.expo, pop_List)
		return self

	def Copy(self):
		import copy
		retu = Term()
		retu.valu = copy.deepcopy(self.valu)
		retu.vari = copy.deepcopy(self.vari)
		retu.expo = copy.deepcopy(self.expo)
		retu.vari.pare = retu
		return retu

	def Orde(self):
		for a in range(len(self.vari)):
			term = self.Copy()
			vari = Vari(term)
			vari.Appe(self.vari[a][0])
			if len(vari) > 0:
				self.vari.pop(a)
				self.vari.Inse(a, vari[0][0], expoInse = False)
		return self

	def Prin(self):
		prin = []
		for a in range(len(self.vari)):
			prin.append(self.vari[a][0])
			prin.append(self.expo[a])
		print(prin, self.valu)

class Equa(list):

	def __init__(self, init = None):
		if init == None:
			init = Term()
		self.Appe(init)

	def Appe(self, appe):
		if type(appe) == Term:
			self.append(appe)
		elif type(appe) == Equa:
			for a in range(len(appe)):
				self.append(appe[a])

	def __add__(self, othe):
		retu = self.Copy()
		if type(othe) == Term:
			retu = othe + retu
		elif type(othe) == Equa:
			for a in range(len(othe)):
				retu = othe[a] + retu
		retu.Clea()
		return retu

	def __iadd__(self, othe):
		retu = self.Copy()
		if type(othe) == Term:
			retu = othe + retu
		elif type(othe) == Equa:
			for a in range(len(othe)):
				retu = othe[a] + retu
		retu.Clea()
		return retu

	def __sub__(self, othe):
		retu = self.Copy()
		if type(othe) == Term:
			retu = othe - retu
		elif type(othe) == Equa:
			for a in range(len(othe)):
				retu = othe[a] - retu
		retu.Clea()
		return retu
	def __isub__(self, othe):
		retu = self.Copy()
		if type(othe) == Term:
			retu = othe - retu
		elif type(othe) == Equa:
			for a in range(len(othe)):
				retu = othe[a] - retu
		retu.Clea()
		return retu

	def __mul__(self, othe):
		retu = Equa()
		if type(othe) == Term:
			for a in range(len(self)):
				retu += self[a] * othe
		elif type(othe) == Equa:
			for a in range(len(self)):
				for b in range(len(othe)):
					retu += self[a] * othe[b]
		retu.Clea()
		return retu

	def __imul__(self, othe):
		retu = Equa()
		if type(othe) == Term:
			for a in range(len(self)):
				retu += self[a] * othe
		elif type(othe) == Equa:
			for a in range(len(self)):
				for b in range(len(othe)):
					retu += self[a] * othe[b]
		retu.Clea()
		return retu

	def __truediv__(self, othe):
		retu = Equa()
		if type(othe) == Term:
			for a in range(len(self)):
				retu += self[a] / othe
		elif type(othe) == Equa:
			for a in range(len(self)):
				for b in range(len(othe)):
					retu += self[a] / othe[b]
		retu.Clea()
		return retu
	def __itruediv__(self, othe):
		retu = Equa()
		if type(othe) == Term:
			for a in range(len(self)):
				retu += self[a] / othe
		elif type(othe) == Equa:
			for a in range(len(self)):
				for b in range(len(othe)):
					retu += self[a] / othe[b]
		retu.Clea()
		return retu

	def Subs(self, vari, equa):
		retu = Equa()
		add_List = []
		for a in range(len(self)):
			term = self[a].Copy()
			othe = Term()
			othe.valu = term.valu
			expo = 0
			valu = 1.0
			foun = False
			for b in range(len(term.vari)):
				if term.vari[b][0] == vari:
					valu = term.valu
					expo = term.expo[b]
					foun = True
				else:
					othe.vari.Appe(term.vari[b][0])
					othe.expo[len(othe.expo) - 1] = term.expo[b]
			if foun == True:
				equ2 = equa.Copy()
				for b in range(1, expo):
					equ2 *= equa
				if expo == 0:
					term = Term()
					term.valu = 1.0
					equ2 = Equa(term)
				retu += equ2 * othe
			else:
				add_List.append(a)
		for a in range(len(add_List)):
			retu.Appe(self[add_List[a]].Copy())
		return retu
					

	def Clea(self):
		self.Sort()
		self.Simp()
		self.Orde()

	def Sort(self):
		for a in range(len(self)):
			self[a].Sort()
		return self

	

	def Simp(self):
		for a in range(len(self)):
			self[a].Simp()
		self.Orde()

		self.SimpSums()
		self.SimpNume()
		self.SimpZero()

	# a*b + a*b -> 2*a*b
	def SimpSums(self):
		pop_List = []
		for a in range(len(self) - 1):
			for b in range(a + 1, len(self)):
				#variPop_List = []
				if (self[a].vari == self[b].vari):
					if (self[a].expo == self[b].expo):
						self[a].valu += self[b].valu
						pop_List.append(b)
		self = Pop_(self, pop_List)
		return self

	def SimpNume(self):
		pop_List = []
		firs = -1
		for a in range(len(self)):
			if len(self[a].vari) == 0:
				if firs == -1:
					firs = a
				else:
					self[firs].valu += self[a].valu
					pop_List.append(a)
		self = Pop_(self, pop_List)
		return self

	def SimpZero(self):
		pop_List = []
		for a in range(len(self)):
			if self[a].valu == 0.0:
				pop_List.append(a)
		self = Pop_(self, pop_List)
		return self

	def Orde(self):
		#retu = self.Copy()
		for a in range(len(self)):
			self[a].Orde()
		return self

	def Copy(self):
		for a in range(len(self)):
			self[a].Copy()
		return self

	def Prin(self):
		if len(self) == 0:
			print("[]")
		else:
			for a in range(len(self)):
				self[a].Prin()

	def PrinStri(self):
		retu = ""
		if len(self) > 0:
			for a in range(len(self)):
				retu += str(self[a].valu)
				if len(self[a].vari) > 0:
					retu += "*"
				for b in range(len(self[a].vari)):
					vari = self[a].vari[b][0]
					if type(vari) != str:
						vari = str(vari)
					fact = False
					if len(vari) > 0 and vari[0] == "!":
						fact = True
						vari = vari[1:len(vari)]
					retu += vari
					if fact == True:
						retu += "!"
					if self[a].expo[b] != 1:
						retu += "^(" + str(self[a].expo[b]) + ")"
					if b < len(self[a].vari) - 1:
						retu += "*"
				if a < len(self) - 1 and self[a + 1].valu >= 0.0:
					retu += "+"
		print(retu)

#################################

# MISC SOLVING

# find the common integer that a LIST OF INTEGERS divides into
def DenoComm(lis_):
	lis_ = sorted(lis_)
	listNew = []
	for inte in lis_:
		listNew.insert(0, inte)
	deno = 1
	for numb in listNew:
		tole = 0.0001
		resu = deno / numb
		floo = resu - int(resu)
		if floo >= tole:
			deno *= numb
	return deno

# simple expander
def ExpaSimp(ter1, ter2):
	retu = ""
	ter1 = Pars(ter1)
	ter2 = Pars(ter2)
	for te1 in ter1:
		for te2 in ter2:
			term = te1 + "*" + te2
			tern = ""
			for a in range(len(term)):
				if term[a] != "*":
					tern += term[a]
			tern = ImagSort(tern)
			term = ""
			for a in range(len(tern)):
				term += tern[a]
			if retu != "" and term[0] != "-":
				retu += "+"
			retu += term
	return retu

def ImagSort(term):
	imag = ""
	tern = ""
	for a in range(len(term)):
		if term[a] == "i" or term[a] == "j" or term[a] == "k":
			imag += term[a]
		else:
			tern += term[a]
	tern = sorted(tern)
	term = ""
	for a in range(len(tern)):
		term += tern[a]
	term += imag
	return term

def Pars(term):
	retu = []
	empt = True
	vari = ""
	for a in range(len(term)):
		if term[a] != " ":
			if vari == "" or empt == True:
				if term[a] != "+":
					vari = term[a]
				empt = False
			else:
				if term[a] == "+" or term[a] == "-":
					retu.append(vari)
					if term[a] == "+":
						vari = ""
					else:
						vari = "-"
				else:
					vari += term[a]
	retu.append(vari)
	return retu

# ij=k
# ji=-k
# jk=i
# kj=-i
# ki=j
# ik=-j
def Imag(ter1, ter2):
	retu = ""
	nega = False
	if len(ter1) > 0 and len(ter2) > 0:
		if ter1[0] == "-" or ter2[0] == "-":
			if ter1[0] != "-" or ter2[0] != "-":
				nega = True
			if ter1[0] == "-":
				ter1 = ter1[1]
			if ter2[0] == "-":
				ter2 = ter2[1]
		if ter1.isalpha() and ter2.isalpha():
			if ter1 == ter2:
				if nega == False:
					retu = "-1"
				else:
					retu = "1"
			if ter1 == "i" and ter2 == "j":
				if nega == False:
					retu = "k"
				else:
					retu = "-k"
			if ter1 == "j" and ter2 == "i":
				if nega == False:
					retu = "-k"
				else:
					retu = "k"
			if ter1 == "j" and ter2 == "k":
				if nega == False:
					retu = "i"
				else:
					retu = "-i"
			if ter1 == "k" and ter2 == "j":
				if nega == False:
					retu = "-i"
				else:
					retu = "i"
			if ter1 == "k" and ter2 == "i":
				if nega == False:
					retu = "j"
				else:
					retu = "-j"
			if ter1 == "i" and ter2 == "k":
				if nega == False:
					retu = "-j"
				else:
					retu = "j"
		else:
			if ter1.isalpha():
				if not ter2.isalpha():
					if nega == False:
						retu = ter1
					else:
						retu = "-" + ter1
			if not ter1.isalpha():
				if ter2.isalpha():
					if nega == False:
						retu = ter2
					else:
						retu = "-" + ter2
			if not ter1.isalpha() and not ter2.isalpha():
				if nega == False:
					retu = "1"
				else:
					retu = "-1"
	return retu

#################################

# counter
# baseList is the max number for each digit
# current is the base 10 progress of the count sequence
# to make a base 2 counter from 0 to 7:
# baseList = [2, 2, 2]
# if len(baseList) > 0:
# 	end = baseList[0]
# a = 1
# while a < len(baseList):
# 	end *= baseList[a]
# 	a += 1
# a = 0
# while a < end:
# 	print(Coun(baseList, a))
# 	a += 1
# this function can be used to continue the progress of an integer incrementing through nested loops that have different sizes
def Coun(baseList, curr):
	retu = []
	size = 1
	a = 0
	while a < len(baseList):
		size = 1
		b = len(baseList) - 1
		while b > a:
			size *= baseList[b]
			b -= 1
		c = baseList[a]
		while c > 0:
			if c * size <= curr:
				retu.append(c)
				curr -= c * size
				break
			c -= 1
		if c == 0:
			retu.append(0)
		a += 1
	return retu

#################################

# 2D INVERSE KINEMATICS

# axle has to directly under the hip or shoulder in (x or y) for this to work
# place bones directly underneath (x and y) the root bone. (elbow goes directly under shoulder, wrist directly under elbow, hand tip directly under wrist)
# ik solution:
# form two right triangles with the line from hip to target (foot) as the base
# a**2 + b**2 = c**2
# a1**2 + b1**2 = c1**2
# a2**2 + b2**2 = c2**2
# b1**2 = c1**2 - a1**2
# b2**2 = c2**2 - a2**2
#	b1 = b2
# c1**2 - a1**2 = c2**2 - a2**2
#	a1 + a2 = A
#	a1 = A - a2
# c1**2 - (A - a2)**2 = c2**2 - a2**2
# c1**2 - (A**2 - 2Aa2 + a2**2) = c2**2 - a2**2
# c1**2 - A**2 + 2Aa2 - a2**2 = c2**2 - a2**2
# c1**2 - A**2 + 2Aa2 = c2**2
# 2Aa2 = c2**2 - c1**2 + A**2
# a2 = (c2**2 - c1**2 + A**2) / 2A
# c1 is uppe, c2 is lowe
def Ik2d(arms = False, A = 1.0, angl = 0.0, uppeLeng = 1.0, loweLeng = 1.0):
	import math
	tole = 0.0001
	# solution
	a2 = (loweLeng ** 2.0 - uppeLeng ** 2.0 + A ** 2.0) / (2.0 * A)
	rati = (A - a2) / uppeLeng
	uppeAngl = 0.0
	loweAngl = 0.0
	if math.fabs(rati) <= 1.0 + tole:
		if rati > 1.0:
			#print("tolerance correction")
			rati = 1.0
		if rati < -1.0:
			#print("tolerance correction")
			rati = -1.0
		bend = math.acos(rati)
		uppeAngl = angl + bend
		if arms == True:
			uppeAngl = angl - bend
	else:
		#print("parent bone domain error")
		# straight to target
		uppeAngl = angl
	rati = a2 / loweLeng
	if math.fabs(rati) <= 1.0 + tole:
		if rati > 1.0:
			#print("tolerance correction")
			rati = 1.0
		if rati < -1.0:
			#print("tolerance correction")
			rati = -1.0
		if arms == False:
			loweAngl = angl - uppeAngl - math.acos(rati)
		else:
			loweAngl = angl - uppeAngl + math.acos(rati)
	else:
		#print("child bone domain error")
		if arms == False:
			loweAngl = angl - uppeAngl
	stra = False
	#stra = True
	# points hips at target and set knees to 0.0 (for debugging "angle" var)
	if stra == True:
		uppeAngl = angl
		loweAngl = 0.0
	return uppeAngl, loweAngl

#################################

# RAYCASTING
# TODO:
# works better than ray
# need to add facing options and checks
# add tole / sort options etc. call Boun()
def Ray2(orig, dest, polyList = [], vertList = [], normList = [], centList = [], retuPoin = False):
	import math
	tole = 0.0001
	anglTole = 0.01
	inte = False
	poin = (0.0, 0.0, 0.0)
	a = 0
	while a < len(polyList):
		vect = Vect(orig, dest)
		magn = VectMagn(vect)
		vect = VectNorm(vect)
		dist = DistVectPlan(orig, vect, centList[a], normList[a])
		if type(dist) == float and dist > 0.0 and dist < magn:
			poin = VectScal(vect, dist)
			poin = VectAdd_(poin, orig)
			# TODO: assumes polygons are sorted by angle
			vectList = []
			leng = len(polyList[a])
			for b in range(leng):
				head = vertList[polyList[a][b]]
				vectList.append(Vect(poin, head))
			angl = 0.0
			for b in range(leng - 1):
				angl += VectAngl(vectList[b], vectList[b + 1])
			angl += VectAngl(vectList[leng - 1], vectList[0])
			if math.fabs(360.0 - angl) < anglTole:
				inte = True
				break
		a += 1
	retu = inte
	if retuPoin == True:
		retu = [inte, poin]
	return retu

# is an obstacle between orig and dest. polyList, vertList, normList, and centList are the geometry lists of obstructing objects. Ray_() returns True if the ray between orig and dest intersected the geometry in the lists.
# magnTole: magnitude tolerance. how far past the difference between origin and destination can the ray travel and be considered in range
def Ray_(orig = (0.0, 0.0, 0.0), dest = (1.0, 0.0, 0.0), polyList = [], vertList = [], normList = [], centList = [], tole = 0.001, magnTole = 5.0, back = False, sort = False):
	pi = 3.14159265359
	# ray direction
	dire = Vect(orig, dest)
	magn = VectMagn(dire)
	# normalized ray direction
	unit = VectNorm(dire)
	boun = False
	a = 0
	while a < len(polyList):
		poly = polyList[a]
		# get the world normal direction
		norm = normList[a]
		# get the world location of the poly center
		cent = centList[a]
		# get the vertices that make up the polygon
		ver_List = []
		for b in range(len(poly)):
			ver_List.append(vertList[poly[b]])
		# is the ray facing the poly
		faci = Faci(unit, orig, cent)
		if faci == True:
			# is the poly facing the ray. setting back to True allows rays to pass through the back of polys
			if back == True:
				faci = Faci(norm, cent, orig)
			else:
				faci = True
			if faci == True:
				# get the distance to the point where the ray intersects the infinite plane in the direction and location of the poly
				dist = DistVectPlan(orig, unit, cent, norm)
				if dist != "divide by zero error":
					if dist <= magn + magnTole:
						# scale the ray by distance
						poin = VectScal(unit, dist)
						# move the vector to the ray origin to get a ray that starts at ray origin and ends where the ray intersects the poly
						poin = VectAdd_(orig, poin)

						#print(orig, dest, polyList, vertList, normList, centList)

						# true or false. is the new vector inside the edges of the poly
						boun = Boun(ver1 = ver_List[0], ver2 = ver_List[1], ver3 = ver_List[2], poin = poin, sort = sort, tole = tole)
						if boun == True:
							break
		a += 1
	# False - the ray missed all polys. True - the ray hit a poly.
	return boun

# is a 3d point inside a 3d triangle
# sort: sort the vectors that start at poin and end at ver1, ver2, and ver3 so that it can be checked if the total angle between sequential vectors is 360.0 degrees. Blender arranges the vertices stored in a polygon list "counter-clockwise" so that sorting isnt necessary. if the vertices are not pre-sorted, set sort to True and the function will sort them.
def Boun(poin = (0.0, 0.0, 0.0), ver1 = (0.0, 0.0, 0.0), ver2 = (0.0, 0.0, 0.0), ver3 = (0.0, 0.0, 0.0), sort = False, tole = 0.001):
	import math
	vec1 = Vect(poin, ver1)
	vec2 = Vect(poin, ver2)
	vec3 = Vect(poin, ver3)
	retu = False
	anglList = []
	# TODO: not well-tested
	if sort == True:
		vectList = [vec1, vec2, vec3]
		if len(vectList) > 1:
			# cross first two vectors to get an axis
			axis = VectCros3d__(vectList[0], vectList[1])
			axis = VectNorm(axis)
			# rotate first vector by 90 to get a reference vector (to know what ""quadrant"" a vector is in)
			refe = Quat(vectList[0], 90.0, axis)
			anglList = [[0.0, vectList[0]]]
			a = 1
			while a < len(vectList):
				# get angle to first vector and an angle to a reference vector
				angl = VectAngl(vectList[a], vectList[0])
				angr = VectAngl(vectList[a], refe)
				# if the angle to the reference vector is greater than 90, make it negative, then ""normalize"" it
				if angr > 90.0:
					angl = (-1.0 * angl) + 360.0
				anglList.append([angl, vectList[a]])
				a += 1
			anglList = sorted(anglList)
	else:
		anglList = [[0.0, vec1], [0.0, vec2], [0.0, vec3]]
	# add the angles between subsequent vectors
	tota = 0.0
	a = 1
	while a < len(anglList):
		add_ = VectAngl(anglList[a - 1][1], anglList[a][1])
		if type(add_) == float:
			tota += add_
		a += 1
	a -= 1
	if len(anglList) > a:
		add_ = VectAngl(anglList[a][1], anglList[0][1])
		if type(add_) == float:
			tota += add_
	# if the total angle between subsequent vectors is 360.0, the point is inside the triangle
	if math.fabs(tota - 360.0) < tole:
		retu = True
	return retu

# convert a bounding box to a triangulated cube
def BounTo__Geom(bbxp, bbxn, bbyp, bbyn, bbzp, bbzn):
	vert = [(bbxn, bbyn, bbzn), (bbxn, bbyn, bbzp), (bbxn, bbyp, bbzn), (bbxn, bbyp, bbzp), (bbxp, bbyn, bbzn), (bbxp, bbyn, bbzp), (bbxp, bbyp, bbzn), (bbxp, bbyp, bbzp)]
	norm = [(-1.0, 0.0, 0.0), (0.0, 1.0, -0.0), (1.0, 0.0, -0.0), (0.0, -1.0, 0.0), (0.0, 0.0, -1.0), (0.0, 0.0, 1.0), (-1.0, 0.0, 0.0), (0.0, 1.0, -0.0), (1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, -1.0), (0.0, -0.0, 1.0)]
	edge = [(0, 2), (0, 1), (1, 3), (2, 3), (2, 6), (3, 7), (6, 7), (4, 6), (5, 7), (4, 5), (0, 4), (1, 5), (1, 2), (3, 6), (4, 7), (0, 5), (0, 6), (3, 5)]
	poly = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5]]
	cent = []
	for a in range(len(poly)):
		cent.append(VectAver(poly[a]))
	return vert, cent, norm, edge, poly

#################################

# SHORTEST PATH

# TODO: work in progress

def PathShor(vert_list, edge_list, star, fini):
	retu = []
	star_all = []
	fini_all = []
	connecte = VertNeig(vert_list, edge_list)
	# find all vertices that connect to the start vertex
	star_all = vert_Neig(star, vert_list, edge_list, star_all)
	# find all vertices that connect to the end vertex
	fini_all = vert_Neig(fini, vert_list, edge_list, fini_all)
	conn = False
	# if start and end are connected
	for a in range(len(star_all)):
		path = star_all[a][0]
		# for all verts in the path
		for b in range(len(path)):
			vers = path[b]
			if vers == fini:
				conn = True
				retu = [star, fini]
	while conn == False:
		conn_all = []
		# update connected (again).
		a = 0
		while a < len(star_all):
			# get the connected vertex path
			star = star_all[a][0]
			# for all verts in the path
			if 1 == 0:
				b = conn_all[a][3]
			else:
				b = 0
			while b < len(star):
				vers = star[b]
				# get the connected vertex path
				c = 0
				while c < len(fini_all):
					fini = fini_all[c][0]
					if 1 == 0:
						d = conn_all[a][4]
					else:
						d = 0
					while d < len(fini):
						verf = fini[d]
						# if any connected or starting verts from either lists are in common, record the indices
						if vers == verf:
							if 1 == 0:
								conn_all[a] = [a, c, vers, b - 1, d - 1]
							else:
								conn_all.append([a, c, vers, b - 1, d - 1])
						d += 1
					c += 1
				b += 1
			a += 1
		# record the smallest distance of any path length in start plus any path length in fini
		smallest = 10000.0
		s = -1
		f = -1
		for a in range(len(star_all)):
			for c in range(len(fini_all)):
				# get star to fini, purge duplicates, and get the path distance
				this_path = []
				for b in range(len(star_all[a][0])):
					this_path.append(star_all[a][0][b])
				for b in range(len(fini_all[c][0])):
					this_path.append(fini_all[c][0][b])
				this_path = sorted(this_path)
				b = 0
				while b < len(this_path) - 1:
					if this_path[b] == this_path[b + 1]:
						this_path.pop(b + 1)
						b = -1
					b += 1
				dis = 0.0
				for b in range(len(this_path) - 1):
					dis += dist(vert_list, this_path[b], this_path[b + 1])
				if dis < smallest:
					smallest = dis
					s = a
					f = c
		# if the shortest path is also connected, the shortest path has been found
		for a in range(len(conn_all)):
			if s == conn_all[a][0] and f == conn_all[a][1]:
				conn = True
		# if the shortest path has been found, build the vert list and exit the loop
		if conn == True:
			verts = []
			for vert in star_all[s][0]:
				verts.append(vert)
			for vert in fini_all[f][0]:
				verts.append(vert)
			retu = verts
			break
		# if the shortest path has not been found, continue building connected paths
		if conn == False:
			a = 0
			while a < len(star_all):
				star_conn = star_all[a][2]
				# if the path is not connected to any path in fini_all
				if star_conn == False:
					# get the vert path
					star = star_all[a][0]
					# get the last vert of the path
					vers = star[len(star) - 1]
					conn_list = []
					# find a new vert connected to vers
					b = 0
					while b < len(edge_list):
						edge = edge_list[b]
						check = -1
						if edge[0] == vers:
							check = edge[1]
						if edge[1] == vers:
							check = edge[0]
						if check != -1:
							# if the vert is not already in the path, add it
							exists = False
							c = 0
							while c < len(star):
								if star[c] == check:
									exists = True
								c += 1
							if exists == False:
								conn_list.append(check)
						b += 1
					star_new = []
					b = 0
					while b < len(conn_list):
						# get the edge distance
						dis = dist(vert_list, vers, conn_list[b])
						star_copy = star[:]
						# add the new edge to the path
						star_copy.append(conn_list[b])
						# add a new entry to the start list
						star_new.append([star_copy, star_all[a][1] + dis, False])
						b += 1
				a += 1
			a = 0
			while a < len(fini_all):
				fini_conn = fini_all[a][2]
				if fini_conn == False:
					fini = fini_all[a][0]
					verf = fini[len(fini) - 1]
					conn_list = []
					b = 0
					while b < len(edge_list):
						edge = edge_list[b]
						check = -1
						if edge[0] == verf:
							check = edge[1]
						if edge[1] == verf:
							check = edge[0]
						if check != -1:
							exists = False
							for c in range(len(fini)):
								if fini[c] == check:
									exists = True
							if exists == False:
								conn_list.append(check)
						b += 1
					fini_new = []
					b = 0
					while b < len(conn_list):
						# get the edge distance
						dis = dist(vert_list, verf, conn_list[b])
						fini_copy = fini[:]
						# add the new edge to the path
						fini_copy.append(conn_list[b])
						# add a new entry to the list
						fini_new.append([fini_copy, fini_all[a][1] + dis, False])
						b += 1
				a += 1
			# update connected
			a = 0
			while a < len(star_all):
				star = star_all[a][0]
				b = 0
				while b < len(star):
					vers = star[b]
					c = 0
					while c < len(fini_all):
						fini = fini_all[c][0]
						d = 0
						while d < len(fini):
							verf = fini[d]
							if vers == verf:
								star_all[a][2] = True
								fini_all[c][2] = True
							d += 1
						c += 1
					b += 1
				a += 1
			# connected paths were skipped earlier, so add them to the new list here
			a = 0
			while a < len(star_all):
				star = star_all[a][2]
				if star == True:
					star_new.append(star_all[a])
				a += 1
			a = 0
			while a < len(fini_all):
				fini = fini_all[a][2]
				if fini == True:
					fini_new.append(fini_all[a])
				a += 1
			star_all = star_new
			fini_all = fini_new
	return retu

def ConnUpda():
	connAll_ = []
	# update connected
	a = 0
	while a < len(starAll_):
		# get the connected vertex path
		star = starAll_[a][0]
		# for all verts in the path
		b = 0
		while b < len(star):
			vers = star[b]
			# get the connected vertex path
			c = 0
			while c < len(finiAll_):
				fini = finiAll_[c][0]
				d = 0
				while d < len(fini):
					verf = fini[d]
					# if any connected or starting verts from either lists are in common, record the indices
					if vers == verf:
						connAll_.append((a, c, vers))
					d += 1
				c += 1
			b += 1
		a += 1

# TODO
def VertConn(vert, vertList, edgeList, retu, get_Dist = False):
	a = 0
	while a < len(edgeList):
		edge = edgeList[a]
		if edge[0] == vert:
			if get_Dist:
				#dis = dist(vertList, vert, edge[1])
				pass
			else:
				dis = 0.0
			# path, total running distance of path, True if path is completed
			retu.append([[vert, edge[1]], dis, False])
		if edge[1] == vert:
			if get_Dist:
				#dis = dist(vertList, vert, edge[0])
				pass
			else:
				dis = 0.0
			retu.append([[vert, edge[0]], dis, False])
		a += 1
	return retu

# TODO
def VertCon2(vert, edgeList, retu):
	a = 0
	while a < len(edgeList):
		edge = edgeList[a]
		if edge[0] == vert:
			retu.append(edge[1])
		if edge[1] == vert:
			retu.append(edge[0])
		a += 1
	return retu

def VertNeig(vertList, edgeList):
	retu = []
	a = 0
	while a < len(vertList):
		thisList = []
		b = 0
		while b < len(edgeList):
			edge = edgeList[b]
			if edge[0] == a:
				# path, total running distance of path, True if path is completed
				thisList.append(edge[1])
			if edge[1] == a:
				thisList.append(edge[0])
			b += 1
		retu.append(thisList)
		a += 1
	return retu

def Connecte(vertList, edgeList):
	retu = []
	a = 0
	while a < len(vertList):
		retu.append(VertNeig(vertList, edgeList))
		a += 1
	return retu

#################################

# TODO

def RotaQuatFind():

	# quaternion
	q = "a+b*i*x+b*j*y+b*k*z"
	# 3d point
	p = "i*p+j*q+k*r"
	# quaternion inverted
	qi = "a-b*i*x-b*j*y-b*k*z"

	# expand q*p*qi
	all_terms = ExpaSimp(q, p)
	all_terms = ExpaSimp(all_terms, qi)
	# convert the string to a list
	all_terms = Pars(all_terms)
	all_terms = sorted(all_terms)
	# separate real and imaginary
	imag_terms = []
	real_terms = []
	for term in all_terms:
		i_term = ""
		r_term = ""
		for a in range(len(term)):
			if term[a] == "i" or term[a] == "j" or term[a] == "k":
				i_term += term[a]
			else:
				r_term += term[a]
		imag_terms.append(i_term)
		real_terms.append(r_term)
	# reduce imaginary values
	ima_terms = []
	for term in imag_terms:
		if len(term) > 1:
			firs = Imag(term[0], term[1])
			if len(term) > 2:
				firs = Imag(firs, term[2])
		else:
			firs = term[0]
		ima_terms.append(firs)
	# read sign on ima terms and transfer to real
	for a in range(len(ima_terms)):
		if len(ima_terms[a]) > 1:
			if real_terms[a][0] == "-":
				new_real = ""
				for b in range(1, len(real_terms[a])):
					new_real += real_terms[a][b]
				real_terms[a] = new_real
			else:
				real_terms[a] = "-" + real_terms[a]
			ima_terms[a] = ima_terms[a][1]
	# factor imaginary terms (and imaginary terms that became 1)
	i_terms = []
	j_terms = []
	k_terms = []
	o_terms = []
	for a in range(len(ima_terms)):
		if ima_terms[a] == "i":
			i_terms.append(real_terms[a])
		if ima_terms[a] == "j":
			j_terms.append(real_terms[a])
		if ima_terms[a] == "k":
			k_terms.append(real_terms[a])
		if ima_terms[a] == "1":
			o_terms.append(real_terms[a])
	if sort == True:
		o_terms = sorted(o_terms)
	o_terms = l2s(o_terms)
	print(o_terms)
	if sort == True:
		i_terms = sorted(i_terms)
	i_terms = l2s(i_terms)
	print(i_terms)
	if sort == True:
		j_terms = sorted(j_terms)
	j_terms = l2s(j_terms)
	print(j_terms)
	if sort == True:
		k_terms = sorted(k_terms)
	k_terms = l2s(k_terms)
	print(k_terms)

def l2s(term_list):
	retu_stri = ""
	for a in range(len(term_list)):
		this_term = ""
		if a != 0:
			if term_list[a][0] != "-":
				this_term += "+"
				for b in range(len(term_list[a])):
					this_term += term_list[a][b]
					if b != len(term_list[a]) - 1:
						this_term += "*"
			else:
				for b in range(len(term_list[a])):
					this_term += term_list[a][b]
					if b > 0 and b != len(term_list[a]) - 1:
						this_term += "*"
		else:
			if term_list[a][0] != "-":
				for b in range(len(term_list[a])):
					this_term += term_list[a][b]
					if b != len(term_list[a]) - 1:
						this_term += "*"
			else:
				for b in range(len(term_list[a])):
					this_term += term_list[a][b]
					if b > 0 and b != len(term_list[a]) - 1:
						this_term += "*"
		retu_stri += this_term
	return retu_stri

