
def Path(posi, orie, pathPoly, moveVect, moveMagn, spee, offs, use_GrouCast, use_PosiAdju, use_Orie, use_OrieCons, scen, math, mathutils, Math):

	# read path geometry
	from scri import path_geom
	vertList, edgeList, polyList, normList, polyEdgeList, edgeNormList, edgeRefeList, bordList = path_geom.PathGeom()

	# next world position of collision point at a distance of offs from the object (set offset to 0.0 to test the position of the object itself)
	coll = Math.VectAdd_(posi, Math.VectScal(moveVect, offs))
	# get a vector in the direction of moveVect with the length of spee * moveMagn. (spee is top speed and moveMagn is a factor)
	vect = Math.VectScal(moveVect, spee * moveMagn)
	# position of object after movement and coll are applied
	loca = Math.VectAdd_(coll, vect)

	# get a list of unwalkable polygons (obstructed by doors, for example)
	unwaList = Unwa(scen)

	# index of the polygon the object is over
	edgeExcl = []
	checInte = True
	while checInte:
		checInte = False
		edg1, edg2, edg3, ver1, ver2, ver3, nor1, nor2, nor3, pol1, pol2, pol3 = PolyGeom(pathPoly, polyEdgeList, vertList, edgeList, edgeNormList, edgeRefeList)
		# is the object still within the triangle
		sam1 = Same(ver1, nor1, loca, pathPoly, pol1, Math)
		sam2 = Same(ver2, nor2, loca, pathPoly, pol2, Math)
		sam3 = Same(ver3, nor3, loca, pathPoly, pol3, Math)
		sameList = [sam1, sam2, sam3]
		edg_List = [edg1, edg2, edg3]
		ver_List = [ver1, ver2, ver3]
		nor_List = [nor1, nor2, nor3]
		#bor_List = [bordList[edg1][1], bordList[edg2][1], bordList[edg3][1]]
		refeList = [edgeRefeList[edg1], edgeRefeList[edg2], edgeRefeList[edg3]]
		for a in range(len(sameList)):
			# the object is inside a new polygon. decide next action if the edge is not in the edgeExcl list
			if sameList[a] == False and (edg_List[a] in edgeExcl) == False:
				updaPathPoly = -1
				callPosiAdju = False
				# get the polygons the edge divides. pol2 is -1 if the edge is a border edge
				pol1 = bordList[edg_List[a]][0]
				pol2 = bordList[edg_List[a]][1]
				if pol1 != pathPoly:
					# if pol1 is not in the unwalkable list, set pathPoly to pol1
					if (pol1 in unwaList) == False: updaPathPoly = pol1
					# if pol1 is unwalkable, adjust the objects position to keep it on the path
					else: callPosiAdju = True
				else:
					# if pol2 is a border object
					if pol2 == -1: callPosiAdju = True
					else:
						if (pol2 in unwaList) == False: updaPathPoly = pol2
						else: callPosiAdju = True
				if updaPathPoly != -1:
					pathPoly = updaPathPoly
					# the new polygon needs to be tested in case the object skipped a triangle
					checInte = True
					edgeExcl.append(edg_List[a])
					break
				if use_PosiAdju and callPosiAdju:
					loca = PosiAdju(ver_List[a], nor_List[a], loca, pathPoly != refeList[a], Math)
					checInte = True
					edgeExcl.append(edg_List[a])
					break
			if a == len(sameList) - 1: edgeExcl = []

	loca = Math.VectAdd_(loca, Math.VectScal(moveVect, -1.0 * offs))

	# note: these functions are best used without offset. to use offset and these functions, call Path() twice and split the options between the two functions

	# update the location of the object to lie on the plane of the polygon
	# TODO: adjust final position to adhere to speed. try drawing a vector from previous to new and scaling. what about when the object crosses a polygon?
	if use_GrouCast: loca = GrouCast(vertList[polyList[pathPoly][0]], normList[pathPoly], loca, pathPoly, Math)
	# orient the object to match the normal of the polygon the object is over
	if use_Orie: orie = Orie(vertList[polyList[pathPoly][0]], normList[pathPoly], orie, loca, Math, use_OrieCons, math, mathutils)

	return loca, orie, pathPoly

# read the geometry of the current polygon
def PolyGeom(pathPoly, polyEdgeList, vertList, edgeList, edgeNormList, edgeRefeList):
	# get the edges for the polygon
	edge = polyEdgeList[pathPoly]
	edg1 = edge[0]
	edg2 = edge[1]
	edg3 = edge[2]
	# get a location on each edge
	ver1 = vertList[edgeList[edg1][0]]
	ver2 = vertList[edgeList[edg2][0]]
	ver3 = vertList[edgeList[edg3][0]]
	# get the normals for the polygon
	nor1 = edgeNormList[edg1]
	nor2 = edgeNormList[edg2]
	nor3 = edgeNormList[edg3]
	# get the polygon the normal points to
	pol1 = edgeRefeList[edg1]
	pol2 = edgeRefeList[edg2]
	pol3 = edgeRefeList[edg3]
	return edg1, edg2, edg3, ver1, ver2, ver3, nor1, nor2, nor3, pol1, pol2, pol3

# check if loca is on the same side of pathPoly
def Same(vert, norm, loca, pathPoly, poly, Math):
	samePoly = False
	if poly == pathPoly: samePoly = True
	sameSide = Math.Faci(norm, vert, loca)
	same = False
	if samePoly == sameSide: same = True
	return same

# keep an object on the path
def PosiAdju(vert, norm, loca, inve, Math):
	if inve: norm = Math.VectScal(norm, -1.0)
	faci = Math.Faci(norm, vert, loca)
	if faci == False:
		dist = Math.DistPoinPlan(loca, vert, norm)
		loca = Math.VectAdd_(loca, Math.VectScal(norm, dist))
	return loca

# read a list of unwalkable polygons
def Unwa(scen):
	unwaList = []
	if scen.name + ".unwa" in scen.objects:
		set_Coun = scen.objects[scen.name + ".unwa"]["set_Coun"]
		for a in range(set_Coun):
			unwa = scen.objects[scen.name + ".unwa"]["unwa." + str(a)]
			if unwa:
				star = scen.objects[scen.name + ".unwa"]["unwaStar." + str(a)]
				end_ = scen.objects[scen.name + ".unwa"]["unwaEnd_." + str(a)]
				for b in range(star, end_):
					unwaList.append(scen.objects[scen.name + ".unwa"]["unwa." + str(b)])
	return unwaList

# cast a ray towards the polygon the object is over and return the location
def GrouCast(poin, norm, loca, pathPoly, Math):
	dist = Math.DistVectPlan(loca, Math.VectScal(norm, -1.0), poin, norm)
	if type(dist) == float:
		dist = Math.VectScal(norm, -1.0 * dist)
		loca = Math.VectAdd_(loca, dist)
	return loca

# orient an object in the direction of a polygon normal
def Orie(vert, norm, orie, loca, Math, use_OrieCons, math, mathutils):
	forw = (orie[0][0], orie[1][0], orie[2][0])
	othe = (orie[0][1], orie[1][1], orie[2][1])
	z___ = (orie[0][2], orie[1][2], orie[2][2])
	orie = orie.to_euler()
	variList = []
	variList.append([loca, othe, norm, forw, vert, z___, 'X'])
	variList.append([loca, forw, norm, othe, vert, z___, 'Y'])
	angl = Math.PlanAngl(variList[0][0], variList[0][1], variList[0][2], variList[0][3], variList[0][4], variList[0][5])
	if type(angl) == float:
		orie.rotate_axis(variList[0][6], math.radians(angl))
		matr = orie.to_matrix()
		forw = (matr[0][0], matr[1][0], matr[2][0])
		othe = (matr[0][1], matr[1][1], matr[2][1])
		z___ = (matr[0][2], matr[1][2], matr[2][2])
	angl = Math.PlanAngl(variList[1][0], variList[1][1], variList[1][2], variList[1][3], variList[1][4], variList[1][5])
	if type(angl) == float:
		if use_OrieCons:
			axis = (math.cos(orie[2] + math.pi / 2.0), math.sin(orie[2] + math.pi / 2.0), 0.0)
			quat = mathutils.Quaternion(axis, math.radians(angl))
			orie.rotate(quat)
		else:
			orie.rotate_axis(variList[1][6], math.radians(angl))
	return orie.to_matrix()

