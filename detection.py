import cv2, math, sys
import numpy as np
import lane
from lane import laneRegion

class potHole:
	def __init__(self, pict):
		self.kernel = np.ones((3,3), np.uint8)
		self.pointDic = []
		self.left 	= []
		self.right 	= []
		self.topleft  		= (0, 0) 
		self.topright 		= (0, 0)
		self.bottomleft 	= (0, 0)
		self.bottomright 	= (0, 0)

		# self.org_image = cv2.imread("img.png")
		self.org_image = pict
		self.height, self.width, _ = self.org_image.shape
		self.frame = self.section(self.height, self.width, self.org_image.copy())

	def section(self, h, w, image):
		self.image = image 
		self.h = h
		self.w = w
		self.rev_triangle_cnt = np.array( [ (0, 0), (0, int(3*self.h/4)), (int(self.w/2), int(self.h/4)), (self.w, int(3*self.h/4)), (self.w, 0) ] )
		self.roi = cv2.drawContours(self.image, [self.rev_triangle_cnt], 0, (0,0,0), -1)
		return self.roi
# _________________________________________________________________________________________________________
	def center(self):
		self.focused = self.edgeImage()
		self.lineDrawing(self.focused)
		self.left_slope()
		self.right_slope()
		self.lane_ = laneRegion(self.left, self.right, self.height, self.width)
		self.lanePoints = self.lane_.laneZ()
		self.fin_image = self.drawLane(self.lanePoints)
		return self.fin_image
# _________________________________________________________________________________________________________
	def edgeImage(self):
		self.imgHLS = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HLS)
		self.Lchannel = self.imgHLS[:,:,1]
		self.mask = cv2.inRange(self.Lchannel, 175, 255)
		self.res = cv2.bitwise_and(self.frame, self.frame, mask= self.mask)
		self.gray_image = cv2.cvtColor(self.res, cv2.COLOR_RGB2GRAY) 
		self.dilate = cv2.dilate(self.gray_image, self.kernel, iterations=4)
		self.blur = cv2.GaussianBlur(self.dilate, (7, 7), 0)
		self.canny = cv2.Canny(self.blur, 50, 150)
		self.dilate = cv2.dilate(self.canny, self.kernel, iterations=1)
		return self.dilate
# _________________________________________________________________________________________________________
	def lineDrawing(self, image):
		self.image = image
		self.lines = cv2.HoughLinesP(self.image ,1 ,np.pi/180, 150)
		for self.point in self.lines:
			for self.x1_, self.y1_, self.x2_, self.y2_ in self.point:
				self.lineCalculation([self.x1_, self.y1_, self.x2_, self.y2_])
# _________________________________________________________________________________________________________
	def left_slope(self):
		for self.eleaL in self.left:
			self.slopeaL, self.lineaL = self.eleaL
			for self.elebL in self.left:
				self.slopebL, self.linebL = self.elebL
				self.calc_comp(str(self.slopeaL)[1:], str(self.slopebL)[1:], self.lineaL, self.linebL)
	def right_slope(self):
		for self.eleaR in self.right:
			self.slopeaR, self.lineaR = self.eleaR
			for self.elebR in self.right:
				self.slopebR, self.linebR = self.elebR
				self.calc_comp(str(self.slopeaR)[1:], str(self.slopebR)[1:], self.lineaR, self.linebR)
# _________________________________________________________________________________________________________
	def drawLane(self, points):
		self.a, self.b, self.c, self.d = points
		self.contourPoints = np.array([self.a, self.b, self.d, self.c])
		self.overlay = self.org_image.copy()
		cv2.fillPoly(self.overlay, pts = [self.contourPoints], color =(255,255,255))
		# cv2.drawContours(self.overlay, [self.contourPoints], 0, (0,255,0), 3)
		self.new_image = cv2.addWeighted(self.overlay, 0.4, self.org_image, 1 - 0.4, 0)
		return self.new_image
# _________________________________________________________________________________________________________
	def lineCalculation(self, points1):
		self.points = points1
		self.length = self.calc_dist(self.points)
		self.angle  = self.calc_angle(self.points)
		self.slope  = self.calc_slope(self.points)
		self.flag = True if (self.length>32) and (35<self.angle<160) else False
		if self.flag :
			if self.slope<0:
				self.left.append([self.slope, self.points])
			elif self.slope>0:
				self.right.append([self.slope, self.points])
		return self.flag, self.length, self.angle, self.slope
	def calc_dist(self, points2):
		self.x1, self.y1, self.x2, self.y2 = points2
		self.x = (self.x1 - self.x2) if self.x1>self.x2 else (self.x2 - self.x1)
		self.y = (self.y1 - self.y2) if self.y1>self.y2 else (self.y2 - self.y1)		
		return int((self.x + self.y)/2)
	def calc_angle(self, points3):
		self.x1, self.y1, self.x2, self.y2 = points3
		self.x2 = self.x2 - self.x1
		self.x1 = 0
		self.y1 = self.y2 - self.y1
		self.y2 = 0
		self.x2 = self.x2 - self.x1
		self.a, self.b, self.c = [self.x1, self.y1], [self.x2, self.y2], [self.x2, self.y1]
		self.ang = int(math.degrees(math.atan2(self.c[1]-self.b[1], self.c[0]-self.b[0]) - math.atan2(self.a[1]-self.b[1], self.a[0]-self.b[0])) )
		self.ang = (90 - self.ang) if self.ang>0 else 90 + (self.ang*-1)
		return self.ang
	def calc_slope(self, points4):
		self.x1, self.y1, self.x2, self.y2 = points4
		return (self.y2-self.y1)/(self.x2-self.x1) if (self.x1!=self.x2) and (self.y1!=self.y2) else 0
# _________________________________________________________________________________________________________
	def calc_comp(self, a, b, c, d):
		self.linea = c
		self.lineb = d
		self.x, self.y = self.calc_decimal(a, b)
		if self.x == self.y:
			self.slopeFlag = True
			self.pointDic.append(str(self.lineb))
			# cv2.line(self.blank_image_2 ,(self.lineb[0], self.lineb[1]), (self.lineb[2], self.lineb[3]), (0, 0, 255), 2)
		else:
			self.slopeFlag = False
	def calc_decimal(self, x, y):
		self.a = x
		self.b = y
		self.loca = self.a.find(".")
		self.locb = self.b.find(".")
		self.deca = self.a[self.loca+1:]
		self.decb = self.b[self.locb+1:]
		self.Awhol = self.a[:self.loca]
		self.Bwhol = self.b[:self.locb]
		if len(self.deca) == 1:
			self.deca = self.deca + "0"
		if len(self.decb) == 1:
			self.decb = self.decb + "0"
		elif len(self.deca) >= 2:
			self.deca = self.deca[:2]
		elif len(self.decb) >= 2:
			self.decb = self.decb[:2]
		self.a1 = self.Awhol + "." + self.deca
		self.b1 = self.Bwhol + "." + self.decb
		return self.a1, self.b1
# _________________________________________________________________________________________________________

img = cv2.imread(sys.argv[1])
obj = potHole(img)
new_image = obj.center()
cv2.imwrite("new_image.png", new_image)
# _________________________________________________________________________________________________________