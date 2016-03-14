from Feature import *

class LineSeg(Feature):
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

    def getLength(self):
        return math.sqrt((self.x1-self.x2)**2+(self.y1-self.y2)**2)

    def bboxcheck(self, lineseg):
        smally1=min(self.y1,self.y2)
        bigy1=max(self.y1,self.y2)
        smally2=min(lineseg.y1,lineseg.y2)
        bigy2=max(lineseg.y1,lineseg.y2)
        if smally2>bigy1 or bigy2 < smally1:
            return False
        smallx1=min(self.x1,self.x2)
        bigx1=max(self.x1,self.x2)
        smallx2=min(lineseg.x1,lineseg.x2)
        bigx2=max(lineseg.x1,lineseg.x2)
        if smallx2>bigx1 or bigx2 < smallx1:
            return False
        return True

    def overlap(self, lineseg):
        small = min(self.y1, self.y2)
        big = max(self.y1, self.y2)
        if small<lineseg.y1<big or small<lineseg.y2<big:
            return True
        else:
            return False

    def intersect(self, lineseg):
        xp=False
        if self.x1==self.x2: ## self parallel to y
            #print 'first line seg verticle'
            if lineseg.x1 == lineseg.x2:
                if lineseg.x1 == self.x1:
                	return self.overlap(lineseg)
            else:
                ## Calcuate the y0 based on y = b2x + a2
                b2=(lineseg.y2-lineseg.y1)/(lineseg.x2-lineseg.x1);
                a2=lineseg.y1-b2*lineseg.x1;
                xp=self.x1;
                yp=a2+b2*xp;
        else: ## self is not parallel to y
            ## Check if otherlineSegment is parallel to y
            if (lineseg.x1==lineseg.x2):
                ## Calcaulate a1 and b1
                b1=(self.y2-self.y1)/(self.x2-self.x1)
                a1=self.y1-b1*self.x1
                xp=lineseg.x1
                yp=a1+b1*xp
            else:
                ## Calculate a1,b1,a2,b2
                b1=(self.y2-self.y1)/(self.x2-self.x1)
                b2=(lineseg.y2-lineseg.y1)/(lineseg.x2-lineseg.x1)
                a1=self.y1-b1*self.x1
                a2=lineseg.y1-b2*lineseg.x1
                if b1==b2:
                    if a1==a2: ## check if two lines overlaps
                        self.overlap(lineseg)
                    else:
                        return False
                else:
                    xp=-(a1-a2)/(b1-b2)
                    yp=a1+b1*xp
        if xp:
            if((self.x1 - xp)*(xp-self.x2)>=0 and (lineseg.x1-xp)*(xp-lineseg.x2)>=0 and (self.y1-yp)*(yp-self.y2)>=0 and (lineseg.y1-yp)*(yp-lineseg.y2)>=0):
                return [xp,yp]
            else:
                #print "x0 and y0 does not meet the conditions"
                return False
        else:
            return False

        


