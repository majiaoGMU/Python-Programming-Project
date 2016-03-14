from Feature import *
from LineSeg import *
from Point import *
import math

class Polyline(Feature):
    def __init__(self):
        pass
    #Considering it may contain multiparts    
    def getLength(self):
        length = 0
        for lineSeg in self.getLineSegs():
            length += lineSeg.getLength()
        return length
    def vis(self, map, color):
        self.transform(map)
        for k in range(self.numParts):
            if (k==self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[k+1]
            tempXYlist = []
            for m in range(self.partsIndex[k], endPointIndex):
                tempXYlist.append(self.winx[m])
                tempXYlist.append(self.winy[m])
            map.can.create_line(tempXYlist, fill=color)

    def visInterLine(self, map, color):
        self.transform(map)
        interSegLine1 = []
        interSegLine2 = []
        for k in range(self.numParts):
            if (k == self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[k+1]
            for m in range(self.partsIndex[k], endPointIndex-1):
                for l in range(polyline.numParts):
                    if (l == polyline.numParts-1):
                        endPointIndexl = polyline.numPoints
                    else:
                        endPointIndexl = polyline.partsIndex[l+1]
                    for n in range(polyline.partsIndex[l], endPointIndexl-1):
                        ls1= LineSeg(self.x[m],self.y[m],self.x[m+1],self.y[m+1])
                        ls2= LineSeg(polyline.x[n],polyline.y[n],polyline.x[n+1],polyline.y[n+1])
                        if ls1.bboxcheck(ls2):
                            interp = ls1.intersect(ls2)
                            if interp:
                                interSegLine1.append(ls1)
                                interSegLine2.append(ls2)
        for v in range(interSegLine1):
            map.can.create_line(interSegLine1[k].x, interSegLine1[v].y, fill=color)
        for t in range(interSegLine2):
            map.can.create_line(interSegLine1[t].x, interSegLine1[t].y, fill=color)

    def bboxcheck(self,polyline):
        if (self.minx>polyline.maxx or self.maxx<polyline.minx or self.miny>polyline.maxy or self.maxy<polyline.miny):
            return False
        else:
            return True
    def intersect(self,polyline):
        interPoints = []
        for k in range(self.numParts):
            if (k == self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[k+1]
            for m in range(self.partsIndex[k], endPointIndex-1):
                for l in range(polyline.numParts):
                    if (l == polyline.numParts-1):
                        endPointIndexl = polyline.numPoints
                    else:
                        endPointIndexl = polyline.partsIndex[l+1]
                    for n in range(polyline.partsIndex[l], endPointIndexl-1):
                        ls1= LineSeg(self.x[m],self.y[m],self.x[m+1],self.y[m+1])
                        ls2= LineSeg(polyline.x[n],polyline.y[n],polyline.x[n+1],polyline.y[n+1])
                        if ls1.bboxcheck(ls2):
                            interp = ls1.intersect(ls2)
                            if interp:
                                interPoints.append(Point(interp[0],interp[1]))                                                                
        return interPoints

    def intersectLine1(self,polyline):
        interLine1 = []
        for k in range(self.numParts):
            if (k == self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[k+1]
                tempXYlist = []
            for m in range(self.partsIndex[k], endPointIndex-1):
                for l in range(polyline.numParts):
                    if (l == polyline.numParts-1):
                        endPointIndexl = polyline.numPoints
                    else:
                        endPointIndexl = polyline.partsIndex[l+1]
                    for n in range(polyline.partsIndex[l], endPointIndexl-1):
                        ls1= LineSeg(self.x[m],self.y[m],self.x[m+1],self.y[m+1])
                        ls2= LineSeg(polyline.x[n],polyline.y[n],polyline.x[n+1],polyline.y[n+1])
                        if ls1.bboxcheck(ls2):
                            interp = ls1.intersect(ls2)
                            if interp:
                                interLine1.append(ls1)
                                
        return interLine1
    

    def intersectLine2(self,polyline):
        interLine2 = []
        for k in range(self.numParts):
            if (k == self.numParts-1):
                endPointIndex = self.numPoints
            else:
                endPointIndex = self.partsIndex[k+1]
            for m in range(self.partsIndex[k], endPointIndex-1):
                for l in range(polyline.numParts):
                    if (l == polyline.numParts-1):
                        endPointIndexl = polyline.numPoints
                    else:
                        endPointIndexl = polyline.partsIndex[l+1]
                    for n in range(polyline.partsIndex[l], endPointIndexl-1):
                        ls1= LineSeg(self.x[m],self.y[m],self.x[m+1],self.y[m+1])
                        ls2= LineSeg(polyline.x[n],polyline.y[n],polyline.x[n+1],polyline.y[n+1])
                        if ls1.bboxcheck(ls2):
                            interp = ls1.intersect(ls2)
                            if interp:
                                interLine2.append(ls2)
                     
        return interLine2

    def transform(self, map): #CENTER
        self.winx, self.winy=[],[]
        centerX = (map.minx+map.maxx)/2
        centerY = (map.maxy+map.miny)/2
        mapCenterX = map.windowWidth/2
        mapCenterY = map.windowHeight/2
        for j in range(self.numPoints):
            self.winx.append((self.x[j]-centerX)*map.ratio+mapCenterX)
            self.winy.append((centerY-self.y[j])*map.ratio+mapCenterY)


    def findBoundingbox(self):
        self.xmin = min(self.x)
        self.ymin = min(self.y)
        self.xmax = max(self.x)
        self.ymax = max(self.y)
