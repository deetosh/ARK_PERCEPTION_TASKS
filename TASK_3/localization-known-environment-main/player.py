from utils import Player,WINDOW_WIDTH
import cv2 as cv
import numpy as np
 

player = Player()
    #Initializing a Player object with a random start position on a randomly generated Maze

def strategy():
    #This function is to localize the position of the newly created player with respect to the map
    Map= player.getMap()
    snapshot=player.getSnapShot()
    # cv.imshow('original_position',snapshot)  #to compare with the final results
    template = snapshot.copy()

    w, h = template.shape[1],template.shape[0]
    res = cv.matchTemplate(Map,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8  #threshhold value can be used nearer to 1 for more accuracy
    loc = np.where( res >= threshold) # creating a list of possible positions by template matching #there can be multiple sections of 51X51 which could be same

    count=0
    #if there are muliple such positions we need to check the surrounding as well
    for pt in zip(*loc[::-1]): 
        
        check=0

        #horizontal--> moving the UAV towards right and comparing
        ct=1
        while player.move_horizontal(1)!=0:
            snapshot_present=player.getSnapShot()
            new_temp= Map[pt[1]:pt[1]+WINDOW_WIDTH,pt[0]+ct:pt[0]+WINDOW_WIDTH+ct]
            diff= cv.subtract(snapshot_present,new_temp)
            ct+=1
            if(cv.countNonZero(diff))>0:  #i.e. snapshot on moving right is not equal to 51x51 image to the right of pt, hence it is not the correct position
                check=1
                break
            

        player.move_horizontal(-ct+1) # recovering the actual position
        if check==1: continue
 
        #horizontal <-- moving the UAV towards left and comparing
        ct=1
        while player.move_horizontal(-1)!=0:
            snapshot_present=player.getSnapShot()
            new_temp= Map[pt[1]:pt[1]+WINDOW_WIDTH,pt[0]-ct:pt[0]+WINDOW_WIDTH-ct]
            diff= cv.subtract(snapshot_present,new_temp)
            ct+=1
            if(cv.countNonZero(diff))>0:
                check=1
                break
            

        player.move_horizontal(ct-1)
        if check==1: continue

        #vertical ^ moving the UAV up and comparing
        ct=1
        while player.move_vertical(1)!=0:
            snapshot_present=player.getSnapShot()
            new_temp= Map[pt[1]+ct:pt[1]+WINDOW_WIDTH+ct,pt[0]:pt[0]+WINDOW_WIDTH]
            diff= cv.subtract(snapshot_present,new_temp)
            ct+=1
            if(cv.countNonZero(diff))>0:
                check=1
                break
            

        player.move_vertical(1-ct)
        if check==1: continue

        #vertical down v moving the UAV down and comparing
        ct=1
        while player.move_vertical(-1)!=0:
            snapshot_present=player.getSnapShot()
            new_temp= Map[pt[1]-ct:pt[1]+WINDOW_WIDTH-ct,pt[0]:pt[0]+WINDOW_WIDTH]
            diff= cv.subtract(snapshot_present,new_temp)
            ct+=1
            if(cv.countNonZero(diff))>0:
                check=1
                break
            

        player.move_vertical(ct-1)
        if check==0: 
            print("present at : ",end="")
            print(str(pt[1]+int(WINDOW_WIDTH/2)) + "," + str(pt[0]+int(WINDOW_WIDTH/2)))   #(vertical distance from top left corner,horizontal distance from top left corner)
            cv.rectangle(Map, pt, (pt[0] + w, pt[1] + h), 0, 2) #to check
            cv.imshow('found',Map) #to check
            cv.waitKey(0)
            return 
         
        count+=1 

if __name__ == "__main__": 
    Start= player.getMap()
    strategy()
    
    

























