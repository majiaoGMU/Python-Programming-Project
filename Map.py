from Layer import *
from Tkinter import *

class Map:
    def __init__(self, winWidth, winHeight):
        self.root=Tk()
        self.root.title("Intersection check for main rivers and freeways in US")
        self.lab = Label(self.root, text = "GGS650_Project Jiao Ma", font = ("COURIER", 10))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.windowWidth, self.windowHeight = winWidth, winHeight
        self.can = Canvas(self.root, height = self.windowHeight, width = self.windowWidth, bg= 'white')
        self.addEvents()
        self.zoomFactor = 1
        self.addButtons()
        self.layers = []
        self.bbxset = False # bounding box
        self.ratio=1
        self.mapMode = 0 #no event: 0; pan: 1
        self.intersectPoints =[]
        self.interSegLine1 = []
        self.interSegLine2 = []

    def calculate(self): #determines ratio, pick bigger one; do it each time a new layer is added
            ratiox = self.windowWidth/(self.maxx-self.minx)
            ratioy = self.windowHeight/(self.maxy-self.miny)
            self.ratio = ratiox
            if self.ratio>ratioy:
                self.ratio = ratioy
            self.ratio /= self.zoomFactor

    def addLayer(self, fileName,color):#creates layer with file name, appends to layers list
        layer = Layer(fileName, color)
        if layer != 0:
            self.layers.append(layer)
            if self.bbxset: #bounding box for map is reset each time a layer is added
                if self.minx > layer.minx:
                    self.minx = layer.minx
                if self.miny > layer.miny:
                    self.miny = layer.miny
                if self.maxx < layer.maxx:
                    self.maxx = layer.maxx
                if self.maxy < layer.maxy:
                    self.maxy = layer.maxy
            else:
                self.minx = layer.minx
                self.miny = layer.miny
                self.maxx = layer.maxx
                self.maxy = layer.maxy
                self.bbxset = True


    def vis(self):
        self.can.delete('all')
        self.calculate()
        for layer in self.layers:
            for feature in layer.features:
                feature.vis(self, layer.color)
        for point in self.intersectPoints:
            xy = self.transform(point)
            self.can.create_oval(xy[0]-3, xy[1]-3, xy[0]+3, xy[1]+3, fill='green')
        for line1 in self.interSegLine1:
            transLine1 = self.transformSeg(line1)
            self.can.create_line(transLine1[0], transLine1[1], transLine1[2], transLine1[3], fill='black', width = '4')
        for line2 in self.interSegLine2:
            transLine2 = self.transformSeg(line2)
            self.can.create_line(transLine2[0], transLine2[1],transLine2[2], transLine2[3], fill='black', width = '4')
        self.can.pack()
        self.lab.pack()

    def transform(self, point):#CENTER
        winx = (point.x-(self.minx+self.maxx)/2)*self.ratio+self.windowWidth/2
        winy = ((self.maxy+self.miny)/2-point.y)*self.ratio+self.windowHeight/2
        return winx,winy

    def transformSeg(self, segment):#CENTER
        winx1 = (segment.x1-(self.minx+self.maxx)/2)*self.ratio+self.windowWidth/2
        winy1 = ((self.maxy+self.miny)/2-segment.y1)*self.ratio+self.windowHeight/2
        winx2 = (segment.x2-(self.minx+self.maxx)/2)*self.ratio+self.windowWidth/2
        winy2 = ((self.maxy+self.miny)/2-segment.y2)*self.ratio+self.windowHeight/2
        return winx1,winy1,winx2,winy2

    def addButtons(self):
        butFrame = Frame(self.root) ## create a frame
        butFrame.pack(side=TOP, fill = BOTH)
        def zoomIn():
            print 'zoom in'
            self.zoomFactor /= 2.0
            self.vis()
        def zoomOut():
            self.zoomFactor *= 2.0
            print 'zoom out'
            self.vis()
        def zoomFull():
            print 'zoom full'
            self.zoomFactor = 1.0
            self.vis()
        def pan():
            self.mapMode = 1 #pan map
            print 'pan'
        def checkIntersection(): # check intersection
            starttime = time.clock()
            if (self.layers[1].bboxcheck(self.layers[2])):
                self.intersectPoints = self.layers[1].intersect(self.layers[2])
                self.vis()
            print str(time.clock()-starttime) + ' seconds were spent on checking intersections'
        def checkIntersectLine(): # check intersect line1, line2
            starttime = time.clock()
            if (self.layers[1].bboxcheck(self.layers[2])):
                self.interSegLine1 = self.layers[1].intersectLine1(self.layers[2])
                self.interSegLine2 = self.layers[1].intersectLine2(self.layers[2])
                self.vis()
        def quitHandler():
            self.mapMode = 5 #quit
            print 'GoodBye'
            os._exit(1)

        #no event: 0; pan: 1; drawPoint: 2; drawLine: 3; drawPolygon: 4
        zoomInBut = Button(butFrame, width = 10, height = 1, text='Zoom In',fg="dark grey", command=zoomIn)
        zoomInBut.pack(side = LEFT)
        zoomOutBut = Button(butFrame, width = 10, height = 1, text='Zoom Out',fg="dark grey", command=zoomOut)
        zoomOutBut.pack(side = LEFT)
        zoomFullBut = Button(butFrame, width = 10, height = 1, text='Zoom Full',fg="dark grey", command=zoomFull)
        zoomFullBut.pack(side = LEFT)
        panBut = Button(butFrame, width = 6, height = 1, text='Pan',fg="dark grey", command=pan)
        panBut.pack(side = LEFT)
        checkIntersectionBut = Button(butFrame, width = 15, height = 1, text='Check Intersection',fg="dark grey", command=checkIntersection)
        checkIntersectionBut.pack(side = LEFT)
        checkIntersectLineBut = Button(butFrame, width = 19, height = 1, text='Check Intersecting Segm',fg="dark grey", command=checkIntersectLine)
        checkIntersectLineBut.pack(side = LEFT)
        quitHandlerBut = Button(butFrame, width = 6, height = 1, text='Quit',fg="dark grey", command=quitHandler)
        quitHandlerBut.pack(side = LEFT)

    def addEvents(self):
        global lastx, lasty, lastline
        lastx, lasty,lastline= 0, 0, None

        def mouseDown(event):
            if (self.mapMode==0):
                return
            global lastx, lasty
            lastx, lasty = event.x, event.y

        def mouseMove(event):
            if (self.mapMode == 0):
                return
            elif (self.mapMode == 1):
                global lastx, lasty, lastline
                if (lastline != None):
                    self.can.delete(lastline)
                lastline = self.can.create_line(lastx, lasty, event.x, event.y)
 

        def mouseRls(event):
            global lastx, lasty
            if (self.mapMode == 0):
                return
            elif (self.mapMode == 1):
                xmove = (event.x-lastx)/self.ratio
                ymove = (event.y-lasty)/self.ratio
                self.minx-=xmove
                self.maxx-=xmove
                self.maxy+=ymove
                self.miny+=ymove
                self.vis()

        self.can.bind("<Button-1>",mouseDown)
        self.can.bind("<B1-Motion>", mouseMove)
        self.can.bind("<ButtonRelease-1>",mouseRls)
