from Feature import *

class Point(Feature):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def distance(self, point):
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

    def vis(self, map, color):
        self.transform(map)
        map.can.create_oval(self.winx-3, self.winy-3, self.winx+3, self.winy+3, fill=color, width = 1)

    def transform(self, map): #CENTER 
        self.winx = int((self.x-(map.minx+map.maxx)/2)*map.ratio)+map.windowWidth/2
        self.winy = int(((map.maxy+map.miny)/2-self.y)*map.ratio)+map.windowHeight/2



