
def VertLoca(scen, vert, pathName):
	#import bge
	#scen = bge.logic.getCurrentScene()
	x = scen.objects[pathName + ".vert"]["vert." + str(vert) + ".x"]
	y = scen.objects[pathName + ".vert"]["vert." + str(vert) + ".y"]
	z = scen.objects[pathName + ".vert"]["vert." + str(vert) + ".z"]
	return (x, y, z)

def VertEdge(scen, edge, pathName):
	#import bge
	#scen = bge.logic.getCurrentScene()
	ver1 = scen.objects[pathName + ".edge"]["edge." + str(edge) + ".0"]
	ver2 = scen.objects[pathName + ".edge"]["edge." + str(edge) + ".1"]
	return ver1, ver2

def PolyEdge(scen, pathPoly, pathName):
	#import bge
	#scen = bge.logic.getCurrentScene()
	edg1 = scen.objects[pathName + ".polyEdge"]["polyEdge." + str(pathPoly) + ".0"]
	edg2 = scen.objects[pathName + ".polyEdge"]["polyEdge." + str(pathPoly) + ".1"]
	edg3 = scen.objects[pathName + ".polyEdge"]["polyEdge." + str(pathPoly) + ".2"]
	return edg1, edg2, edg3

def EdgeNorm(scen, edg1, pathName):
	#import bge
	#scen = bge.logic.getCurrentScene()
	x = scen.objects[pathName + ".edgeNorm"]["edgeNorm." + str(edg1) + ".x"]
	y = scen.objects[pathName + ".edgeNorm"]["edgeNorm." + str(edg1) + ".y"]
	z = scen.objects[pathName + ".edgeNorm"]["edgeNorm." + str(edg1) + ".z"]
	return (x, y, z)

def Norm(scen, norm, pathName):
	#import bge
	#scen = bge.logic.getCurrentScene()
	x = scen.objects[pathName + ".norm"]["norm." + str(norm) + ".x"]
	y = scen.objects[pathName + ".norm"]["norm." + str(norm) + ".y"]
	z = scen.objects[pathName + ".norm"]["norm." + str(norm) + ".z"]
	return (x, y, z)

def Edge(scen, edge, pathName):
	#import bge
	#scen = bge.logic.getCurrentScene()
	e1v1 = scen.objects[pathName + ".edge"]["edge." + str(edge) + ".0"]
	e1v2 = scen.objects[pathName + ".edge"]["edge." + str(edge) + ".1"]
	e11x = scen.objects[pathName + ".vert"]["vert." + str(e1v1) + ".x"]
	e11y = scen.objects[pathName + ".vert"]["vert." + str(e1v1) + ".y"]
	e11z = scen.objects[pathName + ".vert"]["vert." + str(e1v1) + ".z"]
	e12x = scen.objects[pathName + ".vert"]["vert." + str(e1v2) + ".x"]
	e12y = scen.objects[pathName + ".vert"]["vert." + str(e1v2) + ".y"]
	e12z = scen.objects[pathName + ".vert"]["vert." + str(e1v2) + ".z"]
	return [(e11x, e11y, e11z), (e12x, e12y, e12z)]

