import struct
from Point import *
from Polyline import *
from Polygon import *
from Layer import *
import time, os

def readShpPoint(layer,fileName): # parameter fileName is the pathfile name without extension
    fileName = fileName + '.shp'
    print fileName
    starttime = time.clock()
    size = os.path.getsize(fileName)
    shpFile=open(fileName,'rb')
    s = shpFile.read(size)
    shpFile.close()
    b = struct.unpack('>i',s[24:28])
    b=b[0]*2
    featNum = (b-100)/28
    shpFile.close()
    layer.minx, layer.miny, layer.maxx, layer.maxy = struct.unpack("<dddd",s[36:68])
    pointer = 100 + 12
    for i in range(0,featNum):
        b = struct.unpack('dd',s[pointer:pointer+16])
        point = Point(b[0],b[1])
        layer.features.append(point)
        pointer += 28
    ts = time.clock()-starttime
    print ' %f seconds' % (ts)
    #return layer

def readShpPolyline(layer,fileName):# parameter fileName is the pathfile name without extension
    indexName = fileName+'.shx'
    fileLength = os.path.getsize(indexName)
    polylineNum = (fileLength-100)/8
    shpFile = open(indexName,"rb")
    recordsOffset = []
    print fileName
    starttime = time.clock()
    shpFile.seek(0)
    s = shpFile.read(fileLength)
    shpFile.close()
    layer.minx, layer.miny, layer.maxx, layer.maxy = struct.unpack("<dddd",s[36:68])
    pointer = 100
    for i in range(0,polylineNum):
        offset = struct.unpack('>i',s[pointer:pointer+4])
        recordsOffset.append(offset[0]*2)
        pointer += 8
    shpFile.close()
    shpFile = open(fileName+'.shp',"rb")
    shpFile.seek(24)
    s = shpFile.read(4)
    header = struct.unpack(">i",s)
    fileLength = header[0]*2
    shpFile.seek(0)
    s = shpFile.read(fileLength)
    shpFile.close()
    for offset in recordsOffset:
        x, y = [], []
        polyline = Polyline()
        pointer = offset + 8 + 4
        polyline.minx,polyline.miny,polyline.maxx,polyline.maxy = struct.unpack('dddd',s[pointer:pointer+32])
        pointer = offset+ 8 + 36
        polyline.numParts, polyline.numPoints = struct.unpack('ii',s[pointer:pointer+8])
        pointer+=8
        str = ''
        for i in range(polyline.numParts):
            str = str + 'i'
        polyline.partsIndex = struct.unpack(str,s[pointer:pointer+polyline.numParts*4])
        pointer += polyline.numParts * 4
        for i in range(polyline.numPoints):
            pointx, pointy = struct.unpack('dd',s[pointer:pointer+16])
            x.append(pointx)
            y.append(pointy)
            pointer += 16
        polyline.x, polyline.y = x, y
        layer.features.append(polyline)
    ts = time.clock() - starttime
    print ' %f seconds' % (ts)
    #return layer

def readShpPolygon(layer,fileName):# parameter fileName is the pathfile name without extension
    indexName = fileName + '.shx'
    shpFile = open(indexName,"rb")
    fileLength = os.path.getsize(indexName)
    polygonNum = (fileLength-100)/8
    recordsOffset = []
    print fileName
    starttime = time.clock()
    shpFile.seek(0)
    s = shpFile.read(fileLength)
    shpFile.close()
    layer.minx, layer.miny, layer.maxx, layer.maxy = struct.unpack("<dddd",s[36:68])
    pointer = 100
    for i in range(0,polygonNum):
        offset = struct.unpack('>i',s[pointer:pointer+4])
        recordsOffset.append(offset[0]*2)
        pointer += 8
    shpFile.close()
    shpFile = open(fileName+'.shp',"rb")
    shpFile.seek(24)
    s = shpFile.read(4)
    header = struct.unpack(">i",s)
    fileLength = header[0]*2
    shpFile.seek(0)
    s = shpFile.read(fileLength)
    shpFile.close()
    for offset in recordsOffset:
        x, y = [], []
        polygon = Polygon()
        pointer = offset + 8 + 4
        polygon.minx,polygon.miny,polygon.maxx,polygon.maxy = struct.unpack('dddd',s[pointer:pointer+32])
        pointer = offset + 8 + 36
        polygon.numParts, polygon.numPoints = struct.unpack('ii',s[pointer:pointer+8])
        pointer += 8
        str = ''
        for i in range(polygon.numParts):
            str = str+'i'
        polygon.partsIndex = struct.unpack(str,s[pointer:pointer+polygon.numParts*4])
        pointer += polygon.numParts*4
        for i in range(polygon.numPoints):
            pointx, pointy = struct.unpack('dd',s[pointer:pointer+16])
            x.append(pointx)
            y.append(pointy)
            pointer+=16
        polygon.x, polygon.y = x, y
        layer.features.append(polygon)
    ts = time.clock()-starttime
    print ' %f seconds' % (ts)
    #return layer
