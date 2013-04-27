from PIL import Image, ImageDraw
import sys, random
import numpy as np

# Functions

def randomColor(alpha):
	rc = (random.randint(0,255),random.randint(0,255),random.randint(0,255),alpha)
	return rc

def drawRandomCircle(image, x=None, y=None, r=None, color=None):
	shape = Image.new('RGBA', image.size)
	draw = ImageDraw.Draw(shape)
	width, height = image.size
	if x==None:
		x = random.randint(0,width-1)
	if y==None:
		y = random.randint(0,height-1)
	if r==None:
		r = random.randint(0,40)
	if color==None:
		color = randomColor(150)
	draw.ellipse((x-r, y-r, x+r, y+r),fill=color)
	image.paste(shape,mask=shape)
	del draw
	del shape
	return (x,y,r,color)

def compareImages(image1, image2):
	diff = 0
	im1 = image1.load()
	im2 = image2.load()

	for x in xrange(image1.size[0]):
		for y in xrange(image1.size[1]):
			p1 = im1[x,y]
			p2 = im2[x,y]
			for i in xrange(len(p1)):
				diff += (p1[i] - p2[i])**2
	return diff

def compareImages2(image1, image2):
	diff = 0
	arr1 = np.array(image1)
	arr2 = np.array(image2)
	farr1 = arr1.ravel()
	farr2 = arr2.ravel()
	nparr1 = np.matrix(farr1)
	nparr2 = np.matrix(farr2)
	diff = np.sum((arr1 - arr2)**2)
	print diff
	return diff

# Config
G = 50000
N = 20

imagename = sys.argv[1]
targetImage = Image.open(imagename).convert('RGBA')

# Start N # of blank candidates
bestScore = -1
bestcandidate = None
moves = []
scores = []
bestcandidate = Image.new("RGBA",targetImage.size, (0,0,0,0))
best = None

# Cycle through k # of generations

for k in xrange(G):
	candidates = []
	scores = []
	moves = []
	print 'Generation: ', (k+1)
	if bestScore == -1:
		for i in xrange(N):
			#newshape = Image.new("RGBA",targetImage.size, (0,0,0,0))
			newcandidate = Image.new("RGBA",targetImage.size, (0,0,0,0))
			#move = drawRandomCircle(newshape)
			move = drawRandomCircle(newcandidate)
			#newcandidate.paste(newshape, mask=newshape)
			moves.append(move)
			candidates.append(newcandidate)
			scores.append( compareImages(targetImage, newcandidate) )
			#del newshape
			del newcandidate
	else:
		for i in xrange(N):
			#newshape = Image.new("RGBA",targetImage.size, (0,0,0,0))
			newcandidate = Image.new("RGBA",targetImage.size, (0,0,0,0))
			newcandidate.paste(bestcandidate)
			#move = drawRandomCircle(newshape)
			move = drawRandomCircle(newcandidate)
			#newcandidate.paste(newshape, mask=newshape)
			moves.append(move)
			candidates.append(newcandidate)
			scores.append( compareImages(targetImage, newcandidate) )
			#del newshape
			del newcandidate

	index = 0
	bindex = 0
	improvement = False
	for s in scores:
		if ((bestScore==-1) or (s <= bestScore)):
			bestScore = s
			bindex = index
			improvement = True
		index += 1
	
	print 'Current score: ', bestScore
	if improvement:
		del bestcandidate
		bestcandidate = Image.new("RGBA",targetImage.size, (0,0,0,0))
		bestcandidate.paste(candidates[bindex])
	else:
		continue





candidates[bindex].show()

