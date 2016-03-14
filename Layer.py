from ReadShapeFile import *
import struct

class Layer:
    def __init__(self, fileName, color):
        self.minx = 0
        self.miny = 0
        self.maxx = 0
        self.maxy = 0
        self.features = []
        self.color = color
        self.loadData(fileName)
    def loadData(self, fileName):
        shpFile = open(fileName + '.shx',"rb")
        shpFile.seek(32)
        s = shpFile.read(4)
        shapeType, = struct.unpack("i",s)
        layer = 0;
        if shapeType==1:
            readShpPoint(self,fileName)
        elif shapeType == 3:
            readShpPolyline(self,fileName)
        elif shapeType == 5:
            readShpPolygon(self,fileName)
        else:
            print 'not a valid shape file' + str(shapeType)
            return 0
    def bboxcheck(self,layer):
        if self.minx>layer.maxx or self.miny>layer.maxy or self.maxx<layer.minx or self.maxy<layer.miny:
            return False
        else:
            return True
    def intersect(self,layer):
        intPoints = []
        for feature1 in self.features:
                for feature2 in layer.features:
                    if feature1.bboxcheck(feature2):
                        retPts = feature1.intersect(feature2)
                        if retPts:
                            for point in retPts:
                                intPoints.append(point)                            
        print "There is %d intersections" %(len(intPoints))
        return intPoints

    def intersectLine1(self,layer):
        interLine1 = []
        for feature1 in self.features:
                for feature2 in layer.features:
                    if feature1.bboxcheck(feature2):
                        retLine1 = feature1.intersectLine1(feature2)
                        if retLine1:
                                interLine1.append(retLine1[0])                                
        print "There is %d intersecting lines" %(len(interLine1))
        print interLine1
        return interLine1

    def intersectLine2(self,layer):
        interLine2 = []
        for feature1 in self.features:
                for feature2 in layer.features:
                    if feature1.bboxcheck(feature2):
                        retLine2 = feature1.intersectLine2(feature2)
                        if retLine2:
                                interLine2.append(retLine2[0])                                
        print "There is %d intersecting lines" %(len(interLine2))
        print interLine2
        return interLine2
    
        
