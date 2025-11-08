import importlib.util
import os

spec = importlib.util.spec_from_file_location("Modu", os.path.expanduser("~") + os.sep + "Documents" + os.sep + "prog" + os.sep + "Pyth" + os.sep + "Modu" + os.sep + "Modu.py")
Modu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Modu)

Pyth = Modu.Pyth
Math = Modu.Math
Blen = Modu.Blen
BlenGame = Modu.BlenGame
Gene = Modu.Gene
Node = Modu.Node

def main():

	import bpy
	import math

	print()

	path = True
	path = False
	if path:

		scenName = "path"
		pathObje = "path"
		charName = "char"
		scenObje = "scen_obje"

		resx = 640
		resy = 480
		scenNew_ = False
		
		scenNew_ = BlenGame.LeveInit(name = scenName, scenNew_ = scenNew_, resx = resx, resy = resy, glsl = False, debu = True, deleCame = True, deleLigh = True)

		# import scene
		dic_ = Blen.Impo(blenFile = "scen/scen/path.blend", ligh = True, came = True)
		#dic_ = Blen.Impo(blenFile = "scen/scen/path_sphe.blend", ligh = True, came = True)

		# create an empty to hold scene variables
		scenObje = BlenGame.ScenObje(charList = [charName], scenObje = scenObje)
		BlenGame.Scri("scri" + os.sep + "scen.py")
		sensList = ["W", "A", "S", "D", "W_T", "A_T", "S_T", "D_T", "LEFT_SHIFT", "RIGHTAXIS", "UPAXIS", "joysAxisRigh", "joysAxisUp__", "look"]
		for sens in sensList: BlenGame.Controllers()["scen"].link(BlenGame.Sensors()[sens])

		Blen.Sele(pathObje)
		scriStri = BlenGame.PathGeom(scenName = scenName, use_Prop = False)
		Pyth.StriTo__File(scriStri, "scri" + os.sep + "path_geom.py")
		#hideList = BlenGame.PathGeom(scenName = scenName, retu = [])
		Blen.Sele(charName)
		BlenGame.Prop(propName = "pathPoly", propType = 'INT')
		BlenGame.Prop(propName = "pathPolyOffs", propType = 'INT')
		BlenGame.Prop(propName = "offs", propType = 'FLOAT', propValu = 0.6)
		BlenGame.Prop(propName = "cont", propType = 'BOOL', propValu = True)
		Blen.RotaSet_((0.0, 0.0, 180.0))

		Blen.Sele("Camera")
		Blen.Name("came")
		Blen.Sele("Lamp")
		Blen.Name("ligh")

		BlenGame.Pref("path")

		impoModu = ["acti.py", "cycl.py", "game.py", "look_x.py", "look_y.py", "Math.py", "move.py", "orie.py", "path.py", "Pyth.py"]
		for a in range(len(impoModu)):
			bpy.ops.text.open(filepath = "code" + os.sep + impoModu[a])
			bpy.data.texts[impoModu[a]].use_module = True
		bpy.ops.text.open(filepath = "scri" + os.sep + "path_geom.py")
		bpy.data.texts["path_geom.py"].use_module = True

	mark = True
	mark = False
	if mark:

		scenName = "path"
		pathObje = "path"
		charName = "char"
		scenObje = "scen_obje"

		resx = 640
		resy = 480
		scenNew_ = False
		
		scenNew_ = BlenGame.LeveInit(name = scenName, scenNew_ = scenNew_, resx = resx, resy = resy, glsl = False, debu = True, deleCame = True, deleLigh = True)

		# import scene
		dic_ = Blen.Impo(blenFile = "scen/scen/path.blend", ligh = True, came = True)

		# create an empty to hold scene variables
		scenObje = BlenGame.ScenObje(charList = [charName], scenObje = scenObje)
		BlenGame.Scri("scri" + os.sep + "scen.py")
		sensList = ["W", "A", "S", "D", "W_T", "A_T", "S_T", "D_T", "LEFT_SHIFT", "RIGHTAXIS", "UPAXIS", "joysAxisRigh", "joysAxisUp__", "look"]
		for sens in sensList: BlenGame.Controllers()["scen"].link(BlenGame.Sensors()[sens])

		Blen.Sele(pathObje)
		scriStri = BlenGame.PathGeom(scenName = scenName, use_Prop = False)
		Pyth.StriTo__File(scriStri, "scri" + os.sep + "path_geom.py")
		#hideList = BlenGame.PathGeom(scenName = scenName, retu = [])
		Blen.Sele(charName)
		BlenGame.Prop(propName = "pathPoly", propType = 'INT')
		BlenGame.Prop(propName = "offs", propType = 'FLOAT', propValu = 0.6)
		BlenGame.Prop(propName = "cont", propType = 'BOOL', propValu = True)
		Blen.RotaSet_((0.0, 0.0, 180.0))

		Blen.Sele(pathObje)
		minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1 = BlenGame.MMXY()
		# start poly
		polyList = BlenGame.PathPolySet_(pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, "mark.star")
		Blen.Sele(charName)
		BlenGame.Prop(propName = "pathPoly", propType = 'INT')
		BlenGame.Prop(propName = "pathPolyOffs", propType = 'INT')

		# unwalkable
		markList = []
		markList.append("mark.unwa.000")
		markList.append("mark.unwa.001")
		hideList = BlenGame.PathUnwa(pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, markList, scenName, [])

		# triggers
		hideList = BlenGame.PathTrig("door.vari", pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, "mark.door", "door", scenName, hideList)
		hideList = BlenGame.PathTrig("swit.vari", pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, "mark.swit", "swit", scenName, hideList)
		Blen.Sele("door")
		BlenGame.Scri("scri" + os.sep + "door.py")
		Blen.Sele("swit.off_")
		BlenGame.Scri("scri" + os.sep + "swit.py")
		BlenGame.Prop(propName = "active__", propType = 'BOOL')
		bpy.context.object.game.properties["active__"].show_debug = True

		BlenGame.Pref("path")
		#Blen.HideList(hideList)

		impoModu = ["acti.py", "cycl.py", "game.py", "look_x.py", "look_y.py", "Math.py", "move.py", "orie.py", "path.py", "Pyth.py"]
		for a in range(len(impoModu)):
			bpy.ops.text.open(filepath = "code" + os.sep + impoModu[a])
			bpy.data.texts[impoModu[a]].use_module = True
		bpy.ops.text.open(filepath = "scri" + os.sep + "path_geom.py")
		bpy.data.texts["path_geom.py"].use_module = True

	char = True
	#char = False
	if char:

		scenName = "path"
		scenObje = "scen_obje"
		pathObje = "path"
		charName = "char"
		resx = 640
		resy = 480
		scenNew_ = False

		scenNew_ = BlenGame.LeveInit(name = scenName, scenNew_ = scenNew_, resx = resx, resy = resy, glsl = False, debu = True, deleLigh = False)
		Blen.SeleAll_(action = 'DESELECT')
		# import scene
		dic_ = Blen.Impo(blenFile = "scen/scen/path.blend")
		Blen.HideList([charName, "path.x", "path.y", "path.z"])
		charName = "matt"

		# create an empty to hold scene variables
		scenObje = BlenGame.ScenObje(charList = [charName], scenObje = scenObje)
		BlenGame.Scri("scri" + os.sep + "scen.py")
		sensList = ["W", "A", "S", "D", "W_T", "A_T", "S_T", "D_T", "LEFT_SHIFT", "RIGHTAXIS", "UPAXIS", "joysAxisRigh", "joysAxisUp__", "look"]
		for sens in sensList: BlenGame.Controllers()["scen"].link(BlenGame.Sensors()[sens])

		# character
		dic_ = Blen.Impo(blenFile = "scen/char/matt/matt.blend")
		Blen.Sele(charName)

		acti = BlenGame.ActiDict()
		acti["armsRadi"] = 0.607
		acti["armsRati"] = 3.854
		acti["legsRadi"] = 2.748
		acti["osci"] = 0.032
		acti["tilt"] = 0.219
		acti["cyclSpee"] = 8.65
		acti["spee"] = 0.25
		BlenGame.Char(loca = (0.0, 0.0, 0.0), dire = "scen/char/matt/", cyclArms = True, acti = [acti])
		Blen.Sele(charName)
		BlenGame.Cont()
		Blen.Sele(charName)
		BlenGame.PropSet_(propName = "cont", propValu = True)
		lookY___Uppe = 2.1
		lookY___Lowe = 0.8
		BlenGame.CharCame(cameName = "Camera", tab = False, faci = (1.0, 0.0), scroSens = 10, lookY___Limi = True, lookY___LimiInve = False, lookY___Uppe = lookY___Uppe, lookY___Lowe = lookY___Lowe, charList = [charName])

		Blen.Sele(charName)
		Blen.Loca((32.0, 21.0, 15.48684))

		Blen.Sele(pathObje)
		scriStri = BlenGame.PathGeom(scenName = scenName, use_Prop = False)
		Pyth.StriTo__File(scriStri, "scri" + os.sep + "path_geom.py")
		#hideList = BlenGame.PathGeom(scenName = scenName, retu = [])
		Blen.Sele(charName)
		BlenGame.Prop(propName = "pathPoly", propType = 'INT')
		BlenGame.Prop(propName = "pathPolyOffs", propType = 'INT')
		BlenGame.Prop(propName = "offs", propType = 'FLOAT', propValu = 0.6)
		Cycl()

		Blen.Sele(pathObje)
		minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1 = BlenGame.MMXY()
		# start poly
		polyList = BlenGame.PathPolySet_(pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, "mark.star")
		Blen.Sele(charName)
		BlenGame.PropSet_(propName = "pathPoly", propValu = polyList[0])
		BlenGame.PropSet_(propName = "pathPolyOffs", propValu = polyList[0])

		# unwalkable
		markList = []
		markList.append("mark.unwa.000")
		markList.append("mark.unwa.001")
		hideList = BlenGame.PathUnwa(pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, markList, scenName, [])

		# triggers
		hideList = BlenGame.PathTrig("door.vari", pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, "mark.door", "door", scenName, hideList)
		hideList = BlenGame.PathTrig("swit.vari", pathObje, minxLis1, minxInd1, maxxLis1, maxxInd1, minyLis1, minyInd1, maxyLis1, maxyInd1, "mark.swit", "swit", scenName, hideList)
		Blen.Sele("door")
		BlenGame.Scri("scri" + os.sep + "door.py")
		Blen.Sele("swit.off_")
		BlenGame.Scri("scri" + os.sep + "swit.py")
		BlenGame.Prop(propName = "active__", propType = 'BOOL')
		bpy.context.object.game.properties["active__"].show_debug = True

		Blen.Sele("Camera")
		Blen.Name("came")
		bpy.ops.transform.translate(value = (0.0, 0.0, 3.0), constraint_axis = (False, False, True), constraint_orientation = 'LOCAL')

		Blen.Sele("Lamp")
		Blen.Name("ligh")
		Blen.Loca((42.0, 6.0, 24.0))
		bpy.context.object.data.energy = 2.0

		BlenGame.Pref(scenName)
		#Blen.HideList(hideList)

		impoModu = ["acti.py", "cycl.py", "game.py", "look_x.py", "look_y.py", "Math.py", "move.py", "orie.py", "path.py", "Pyth.py"]
		for a in range(len(impoModu)):
			bpy.ops.text.open(filepath = "code" + os.sep + impoModu[a])
			bpy.data.texts[impoModu[a]].use_module = True
		bpy.ops.text.open(filepath = "scri" + os.sep + "path_geom.py")
		bpy.data.texts["path_geom.py"].use_module = True

def Cycl():
	BlenGame.PropSet_(propName = "jog_LegsX00", propValu = -1.1715012788772583)
	BlenGame.PropSet_(propName = "jog_LegsY00", propValu = -0.006090658716857433)
	BlenGame.PropSet_(propName = "jog_LegsX01", propValu = -1.133657693862915)
	BlenGame.PropSet_(propName = "jog_LegsY01", propValu = 0.12255960702896118)
	BlenGame.PropSet_(propName = "jog_LegsX02", propValu = -0.6972678899765015)
	BlenGame.PropSet_(propName = "jog_LegsY02", propValu = 0.37646549940109253)
	BlenGame.PropSet_(propName = "jog_LegsX03", propValu = -0.45101505517959595)
	BlenGame.PropSet_(propName = "jog_LegsY03", propValu = 0.39450353384017944)
	BlenGame.PropSet_(propName = "jog_LegsX04", propValu = -0.09052211791276932)
	BlenGame.PropSet_(propName = "jog_LegsY04", propValu = 0.20272567868232727)
	BlenGame.PropSet_(propName = "jog_LegsX05", propValu = 0.05977433919906616)
	BlenGame.PropSet_(propName = "jog_LegsY05", propValu = 0.26926273107528687)
	BlenGame.PropSet_(propName = "jog_LegsX06", propValu = 0.6383165121078491)
	BlenGame.PropSet_(propName = "jog_LegsY06", propValu = 0.3466039299964905)
	BlenGame.PropSet_(propName = "jog_LegsX07", propValu = 0.5497186183929443)
	BlenGame.PropSet_(propName = "jog_LegsY07", propValu = 0.10148997604846954)
	BlenGame.PropSet_(propName = "jog_LegsX08", propValu = 0.7705233693122864)
	BlenGame.PropSet_(propName = "jog_LegsY08", propValu = -0.0678902268409729)
	BlenGame.PropSet_(propName = "jog_LegsX09", propValu = 0.9093456268310547)
	BlenGame.PropSet_(propName = "jog_LegsY09", propValu = -0.003694202285259962)
	BlenGame.PropSet_(propName = "jog_LegsX10", propValu = 0.5004748106002808)
	BlenGame.PropSet_(propName = "jog_LegsY10", propValu = -0.2482115477323532)
	BlenGame.PropSet_(propName = "jog_LegsX11", propValu = 0.15416473150253296)
	BlenGame.PropSet_(propName = "jog_LegsY11", propValu = -0.4601432681083679)
	BlenGame.PropSet_(propName = "jog_LegsX12", propValu = -0.04775390774011612)
	BlenGame.PropSet_(propName = "jog_LegsY12", propValu = -0.12878575921058655)
	BlenGame.PropSet_(propName = "jog_LegsX13", propValu = -0.6007677912712097)
	BlenGame.PropSet_(propName = "jog_LegsY13", propValu = -0.17720341682434082)
	BlenGame.PropSet_(propName = "jog_LegsX14", propValu = -0.8619587421417236)
	BlenGame.PropSet_(propName = "jog_LegsY14", propValu = -0.3732094168663025)
	BlenGame.PropSet_(propName = "jog_LegsX15", propValu = -1.1164268255233765)
	BlenGame.PropSet_(propName = "jog_LegsY15", propValu = -0.23773682117462158)
	"""
	jog_ArmsX00 -0.4153825342655182
	jog_ArmsY00 0.18329185247421265
	jog_ArmsX01 -0.5433993339538574
	jog_ArmsY01 0.2447473704814911
	jog_ArmsX02 -0.16608844697475433
	jog_ArmsY02 0.19038808345794678
	jog_ArmsX03 -0.02691817283630371
	jog_ArmsY03 0.09343209862709045
	jog_ArmsX04 -0.20006194710731506
	jog_ArmsY04 0.18962395191192627
	jog_ArmsX05 -0.031941007822752
	jog_ArmsY05 0.2754628360271454
	jog_ArmsX06 0.4270501434803009
	jog_ArmsY06 0.16202247142791748
	jog_ArmsX07 0.29790809750556946
	jog_ArmsY07 -0.10017912089824677
	jog_ArmsX08 0.601900041103363
	jog_ArmsY08 -0.1966392993927002
	jog_ArmsX09 0.4772917926311493
	jog_ArmsY09 -0.011414635926485062
	jog_ArmsX10 0.16395129263401031
	jog_ArmsY10 0.05079043656587601
	jog_ArmsX11 -0.10217714309692383
	jog_ArmsY11 0.055955350399017334
	jog_ArmsX12 -0.16453146934509277
	jog_ArmsY12 -0.226598858833313
	jog_ArmsX13 -0.33518776297569275
	jog_ArmsY13 -0.03440486639738083
	jog_ArmsX14 -0.5751481056213379
	jog_ArmsY14 -0.25056424736976624
	jog_ArmsX15 -0.5385220050811768
	jog_ArmsY15 0.004304639063775539
	"""

main()

