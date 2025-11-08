
# TODO: moving on a rotated incline changes direction of movement
def Path(posi, orie, pathPoly, moveVect, moveMagn, spee, offs, use_GrouCast, use_PosiAdju, use_Orie, use_OrieCons, scen, math, mathutils, Math, pathObje, debu = False):

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
		use_Prop = scen.objects[scen.name + "." + pathObje]["use_Prop"]
		if use_Prop:
			# read current polygon geometry
			edg1, edg2, edg3, ver1, ver2, ver3, nor1, nor2, nor3, pol1, pol2, pol3 = PolyGeom(scen, pathPoly, pathObje)
			refeList = [EdgeRefeList(scen, edg1, pathObje), EdgeRefeList(scen, edg2, pathObje), EdgeRefeList(scen, edg3, pathObje)]
			vert = VertList(scen, PolyList(scen, pathPoly, pathObje), pathObje)
			norm = NormList(scen, pathPoly, pathObje)
		else:
			# read path geometry. (path geometry is stored to blender properties if use_Prop == True)
			import path_geom
			# read current polygon geometry
			edg1, edg2, edg3, ver1, ver2, ver3, nor1, nor2, nor3, pol1, pol2, pol3 = PolyGeomScri(scen, pathPoly, pathObje, path_geom)
			refeList = [path_geom.EdgeRefeList(inde = edg1), path_geom.EdgeRefeList(inde = edg2), path_geom.EdgeRefeList(inde = edg3)]
			poly = path_geom.PolyList(inde = pathPoly)
			vert = path_geom.VertList(inde = poly[0])
			norm = path_geom.NormList(inde = pathPoly)
		# is the object still within the triangle
		sam1 = Same(ver1, nor1, loca, pathPoly, pol1, Math)
		sam2 = Same(ver2, nor2, loca, pathPoly, pol2, Math)
		sam3 = Same(ver3, nor3, loca, pathPoly, pol3, Math)
		sameList = [sam1, sam2, sam3]
		edg_List = [edg1, edg2, edg3]
		ver_List = [ver1, ver2, ver3]
		nor_List = [nor1, nor2, nor3]
		for a in range(len(sameList)):
			# the object is inside a new polygon. decide next action if the edge is not in the edgeExcl list
			if sameList[a] == False and (edg_List[a] in edgeExcl) == False:
				updaPathPoly = -1
				callPosiAdju = False
				# get the polygons the edge divides. pol2 is -1 if the edge is a border edge
				if use_Prop:
					pol1, pol2 = EdgeBordList(scen, edg_List[a], pathObje)
				else:
					pol1 = path_geom.EdgeBordList(inde = edg_List[a])
					pol2 = pol1[1]
					pol1 = pol1[0]
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
				# TODO:
				# jumping a border edge can prevent the next polygon from being found
				# this should possibly only be called after all edges have been checked
				# can unwalkable cause the same problem
				# reorganize to account for this issue without all the conditions
				# can this be a problem in other cases, like when use_PosiAdju is true?
				brea = False
				if sameList[a] == False and pol2 == -1 and use_PosiAdju == False and offs == 0.0 and use_GrouCast and updaPathPoly == -1:
					for b in range(len(sameList)):
						if b != a and (edg_List[b] in edgeExcl) == False:
							if use_Prop:
								pol3, pol4 = EdgeBordList(scen, edg_List[b], pathObje)
							else:
								pol3 = path_geom.EdgeBordList(inde = edg_List[b])
								pol4 = pol3[1]
								pol3 = pol3[0]
							poly = -1
							if pol3 != pathPoly:
								poly = pol3
							else:
								if pol4 != -1:
									poly = pol4
							if poly != -1:
								pathPoly = poly
								checInte = True
								edgeExcl.append(edg_List[b])
								brea = True
								break
				if brea:
					break
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
	if use_GrouCast: loca = GrouCast(vert, norm, loca, pathPoly, Math)
	
	# orient the object to match the normal of the polygon the object is over
	if use_Orie: orie = Orie(vert, norm, orie, loca, Math, use_OrieCons, math, mathutils)

	return loca, orie, pathPoly

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
				coun = scen.objects[scen.name + ".unwa"]["unwaCoun." + str(a)]
				for b in range(coun):
					unwaList.append(scen.objects[scen.name + ".unwa"]["unwa." + str(a) + "." + str(b)])
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

# read the geometry of the current polygon
def PolyGeomScri(scen, pathPoly, pathObje, path_geom):
	# get the edges for the polygon
	edge = path_geom.PolyEdgeList(inde = pathPoly)
	edg1 = edge[0]
	edg2 = edge[1]
	edg3 = edge[2]
	# get a location on each edge
	ed_1 = path_geom.EdgeList(inde = edg1)
	ed_2 = path_geom.EdgeList(inde = edg2)
	ed_3 = path_geom.EdgeList(inde = edg3)
	ver1 = path_geom.VertList(inde = ed_1[0])
	ver2 = path_geom.VertList(inde = ed_2[0])
	ver3 = path_geom.VertList(inde = ed_3[0])
	# get the normals for the polygon
	nor1 = path_geom.EdgeNormList(inde = edg1)
	nor2 = path_geom.EdgeNormList(inde = edg2)
	nor3 = path_geom.EdgeNormList(inde = edg3)
	# get the polygon the normal points to
	pol1 = path_geom.EdgeRefeList(inde = edg1)
	pol2 = path_geom.EdgeRefeList(inde = edg2)
	pol3 = path_geom.EdgeRefeList(inde = edg3)
	return edg1, edg2, edg3, ver1, ver2, ver3, nor1, nor2, nor3, pol1, pol2, pol3

def PolyGeom(scen, pathPoly, pathObje):
	# get the edges for the polygon
	edg1, edg2, edg3 = PolyEdgeList(scen, pathPoly, pathObje)
	# get a location on each edge
	ver1 = EdgeList(scen, edg1, pathObje)
	ver2 = EdgeList(scen, edg2, pathObje)
	ver3 = EdgeList(scen, edg3, pathObje)
	ver1 = VertList(scen, ver1, pathObje)
	ver2 = VertList(scen, ver2, pathObje)
	ver3 = VertList(scen, ver3, pathObje)
	# get the normals for the polygon
	nor1 = EdgeNormList(scen, edg1, pathObje)
	nor2 = EdgeNormList(scen, edg2, pathObje)
	nor3 = EdgeNormList(scen, edg3, pathObje)
	# get the polygon the normal points to
	pol1 = EdgeRefeList(scen, edg1, pathObje)
	pol2 = EdgeRefeList(scen, edg2, pathObje)
	pol3 = EdgeRefeList(scen, edg3, pathObje)
	return edg1, edg2, edg3, ver1, ver2, ver3, nor1, nor2, nor3, pol1, pol2, pol3

def VertList(scen, vert, pathObje):
	x = scen.objects[scen.name + "." + pathObje + ".vertList"]["vert." + str(vert) + ".x"]
	y = scen.objects[scen.name + "." + pathObje + ".vertList"]["vert." + str(vert) + ".y"]
	z = scen.objects[scen.name + "." + pathObje + ".vertList"]["vert." + str(vert) + ".z"]
	return (x, y, z)

def EdgeList(scen, edge, pathObje, inde = 0):
	return scen.objects[scen.name + "." + pathObje + ".edgeList"]["edge." + str(edge) + "." + str(inde)]

def PolyList(scen, poly, pathObje, inde = 0):
	return scen.objects[scen.name + "." + pathObje + ".polyList"]["poly." + str(poly) + "." + str(inde)]

def NormList(scen, norm, pathObje):
	x = scen.objects[scen.name + "." + pathObje + ".normList"]["norm." + str(norm) + ".x"]
	y = scen.objects[scen.name + "." + pathObje + ".normList"]["norm." + str(norm) + ".y"]
	z = scen.objects[scen.name + "." + pathObje + ".normList"]["norm." + str(norm) + ".z"]
	return (x, y, z)

def PolyEdgeList(scen, pathPoly, pathObje):
	edg1 = scen.objects[scen.name + "." + pathObje + ".polyEdgeList"]["polyEdge." + str(pathPoly) + ".0"]
	edg2 = scen.objects[scen.name + "." + pathObje + ".polyEdgeList"]["polyEdge." + str(pathPoly) + ".1"]
	edg3 = scen.objects[scen.name + "." + pathObje + ".polyEdgeList"]["polyEdge." + str(pathPoly) + ".2"]
	return edg1, edg2, edg3

def EdgeNormList(scen, edg1, pathObje):
	x = scen.objects[scen.name + "." + pathObje + ".edgeNormList"]["edgeNorm." + str(edg1) + ".x"]
	y = scen.objects[scen.name + "." + pathObje + ".edgeNormList"]["edgeNorm." + str(edg1) + ".y"]
	z = scen.objects[scen.name + "." + pathObje + ".edgeNormList"]["edgeNorm." + str(edg1) + ".z"]
	return (x, y, z)

def EdgeRefeList(scen, edge, pathObje):
	return scen.objects[scen.name + "." + pathObje + ".edgeRefeList"]["edgeRefe." + str(edge)]

def EdgeBordList(scen, edge, pathObje):
	pol1 = scen.objects[scen.name + "." + pathObje + ".edgeBordList"]["edgeBord." + str(edge) + ".0"]
	pol2 = scen.objects[scen.name + "." + pathObje + ".edgeBordList"]["edgeBord." + str(edge) + ".1"]
	return pol1, pol2

