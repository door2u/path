
def MoveVect(dire, magn, orie, look, math, Math):
	upda = True
	retu = (0.0, 0.0, 0.0)
	dire += look
	vecx = (orie[0][0], orie[1][0], orie[2][0])
	vecy = (orie[0][1], orie[1][1], orie[2][1])
	vecx = Math.VectScal(vecx, math.cos(math.radians(dire)))
	vecy = Math.VectScal(vecy, math.sin(math.radians(dire)))
	retu = Math.VectNorm(Math.VectAdd_(vecx, vecy))
	if magn == 0.0:
		retu = (0.0, 0.0, 0.0)
		upda = False
	return retu, upda

