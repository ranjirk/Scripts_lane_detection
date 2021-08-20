class laneRegion :

	def __init__(self, left, right, height, width):
		self.left 	= left
		self.right 	= right
		self.height = height
		self.width 	= width

	def laneZ(self):
		self.lanePoints = self.laneLine()
		self.points = self.laneBox(self.lanePoints)
		return self.points
# ______________________________________________________________________________________
	def laneLine(self):
		self.ymin = self.height
		self.xmin = self.width
		self.ymax = 0
		self.xmax = 0
		for self.eleL in self.left:
			self.lineaL = self.eleL[1]
# _________________________________________top most part
			if self.lineaL[1] < self.ymin :
				self.ymin = self.lineaL[1]
			if self.lineaL[3] < self.ymin :
				self.ymin = self.lineaL[3]
# _________________________________________left most part
			if self.lineaL[0] < self.xmin :
				self.xmin = self.lineaL[0]
			if self.lineaL[2] < self.xmin :
				self.xmin = self.lineaL[2]
# _________________________________________bottom most part
			if self.lineaL[1] > self.ymax :
				self.ymax = self.lineaL[1]
			if self.lineaL[3] > self.ymax :
				self.ymax = self.lineaL[3]
# _________________________________________right most part
			if self.lineaL[0] > self.xmax :
				self.xmax = self.lineaL[0]
			if self.lineaL[2] > self.xmax :
				self.xmax = self.lineaL[2]
		self.point_A = (self.xmax, self.ymin)
		self.point_C = (self.xmin, self.ymax)
# ____________________________________________________________
		self.ymin = self.height
		self.xmin = self.width
		self.ymax = 0
		self.xmax = 0

		for self.eleR in self.right:
			self.lineaR = self.eleR[1]
# _________________________________________top most part
			if self.lineaR[1] < self.ymin :
				self.ymin = self.lineaR[1]
			if self.lineaR[3] < self.ymin :
				self.ymin = self.lineaR[3]
# _________________________________________left most part
			if self.lineaR[0] < self.xmin :
				self.xmin = self.lineaR[0]
			if self.lineaR[2] < self.xmin :
				self.xmin = self.lineaR[2]
# _________________________________________bottom most part
			if self.lineaR[1] > self.ymax :
				self.ymax = self.lineaR[1]
			if self.lineaR[3] > self.ymax :
				self.ymax = self.lineaR[3]
# _________________________________________right most part
			if self.lineaR[0] > self.xmax :
				self.xmax = self.lineaR[0]
			if self.lineaR[2] > self.xmax :
				self.xmax = self.lineaR[2]
		self.point_B = (self.xmin, self.ymin)
		self.point_D = (self.xmax, self.ymax)
		return self.point_A, self.point_B, self.point_C, self.point_D
# ______________________________________________________________________________________
	def laneBox(self, points):
		self.A, self.B, self.C, self.D = points
		self.a = [self.A[0]]
		self.b = [self.B[0]]
		self.c = [self.C[0]]
		self.d = [self.D[0]]

		if self.A[1] > self.B[1]:
			self.a.append(self.A[1])
			self.b.append(self.A[1])
		else:
			self.a.append(self.B[1])
			self.b.append(self.B[1])
		if self.C[1] < self.D[1]:
			self.c.append(self.C[1])
			self.d.append(self.C[1])
		else:
			self.c.append(self.D[1])
			self.d.append(self.D[1])

		return [self.a, self.b, self.c, self.d]
# ______________________________________________________________________________________