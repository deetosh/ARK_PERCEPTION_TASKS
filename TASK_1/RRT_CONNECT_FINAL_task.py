import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random

img= cv.imread('photos/maze1.png',0)
np_img= np.array(img)
np_img= ~np_img
np_img[np_img >0]=1


class treeNode():
    def __init__(self, locationX, locationY):
        self.locationX= locationX
        self.locationY= locationY
        self.children = []
        self.parent= None

class rrtAlogo():
    def __init__(self,start,goal,numIterations,grid,stepSize):
        self.randomTree= treeNode(start[0],start[1])
        self.goal= treeNode(goal[0],goal[1])
        self.nearestNode= None
        self.iterations= min(numIterations,10000)
        self.grid= grid
        self.rho = stepSize
        self.path_distance= 0
        self.nearestDist= 10000
        self.numWaypoints=0
        self.waypoints=[]

    def addChild(self,locationX, locationY):
        if (locationX==self.goal.locationX):
            self.nearestNode.children.append(self.goal)
            self.goal.parent= self.nearestNode

        else:
            tempNode = treeNode(locationX,locationY)
            self.nearestNode.children.append(tempNode)
            tempNode.parent=self.nearestNode

    def samplePoint(self):
        x= random.randint(1, grid.shape[1])
        y= random.randint(1, grid.shape[0])
        pt = np.array([x,y])
        return pt
    
    def moveToPoint(self,locationStart,locationEnd):
        offset= self.rho*self.unitVector(locationStart,locationEnd)
        pt= np.array([locationStart.locationX + offset[0],locationStart.locationY + offset[1]])
        if pt[0]>= grid.shape[1]:
            pt[0]= grid.shape[1]
        if pt[1]>=grid.shape[0]:
            pt[1]=grid.shape[0]
        return pt
    
    def isInObstacle(self,locationStart, locationEnd):
        u_hat= self.unitVector(locationStart,locationEnd)
        testPoint = np.array([0.0,0.0])
        for i in range(self.rho):
            testPoint[0]= locationStart.locationX + i*u_hat[0]
            testPoint[1]= locationStart.locationY + i*u_hat[1]
            if 0<round(testPoint[1].astype(np.int64))<self.grid.shape[0] and 0<round(testPoint[0].astype(np.int64))<self.grid.shape[1] and self.grid[round(testPoint[1].astype(np.int64)),round(testPoint[0].astype(np.int64))] == 1:
                return True
        return False
    
    def unitVector(self,locationStart,locationEnd):
        v= np.array([locationEnd[0]-locationStart.locationX,locationEnd[1]-locationStart.locationY])
        u_hat= v/np.linalg.norm(v)
        return u_hat
    
    def findNearest(self,root,point):
        if not root:
            return
        dist= self.distance(root,point)
        if dist<=self.nearestDist:
            self.nearestNode = root
            self.nearestDist = dist

        for child in root.children:
            self.findNearest(child,point)
            pass
            
    def distance(self,node1,point):
        dist= np.sqrt((node1.locationX-point[0])**2+(node1.locationY-point[1])**2)
        return dist
    
    def goalFound(self,point):
        if self.distance(self.goal,point) <= self.rho:
            return True
        pass

    def resetNearestValues(self):
        self.nearestNode=None
        self.nearestDist=10000

    def retraceRRTPath(self,goal):
        if goal.locationX == self.randomTree.locationX:
            return
        self.numWaypoints+=1
        currentPoint= np.array([goal.locationX,goal.locationY])
        self.waypoints.insert(0,currentPoint)
        self.path_distance+=self.rho
        self.retraceRRTPath(goal.parent)

grid= np_img
start= np.array([40.0,300.0])
goal= np.array([80.0,300.0])
numIterations= 10000
stepSize=20

plt.imshow(grid,cmap='binary')
plt.plot(start[0],start[1],'ro')
plt.plot(goal[0],goal[1],'bo')

rrt= rrtAlogo(start,goal,numIterations,grid,stepSize)

for i in range(rrt.iterations):
    rrt.resetNearestValues()

    point = rrt.samplePoint()
    rrt.findNearest(rrt.randomTree,point)
    new=rrt.moveToPoint(rrt.nearestNode,point)
    bool = rrt.isInObstacle(rrt.nearestNode,new)
    if(bool==False):
        rrt.addChild(new[0],new[1])

        if(rrt.goalFound(new)):
            rrt.addChild(goal[0],goal[1])
            print("Goal found!")
            break

rrt.retraceRRTPath(rrt.goal)
rrt.waypoints.insert(0,start)
print("Number of waypoints: ",rrt.numWaypoints)
print("Path Distance(m): ",rrt.path_distance)

for i in range(len(rrt.waypoints)-1):
    plt.plot([rrt.waypoints[i][0], rrt.waypoints[i+1][0]],[rrt.waypoints[i][1],rrt.waypoints[i+1][1]],'b-')
    plt.pause(0.10)

plt.savefig('plot image.png')

plt.show()
