import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import random

# setting the webcam and adjusting the height and width of the frame
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon = 0.8,maxHands=1)

#creating a class is much easier because we can access anything from that..
#We need
#list of points
#list of distances
#current length
#total length
class SnakeGameClass:
    def __init__(self,pathFood):
        self.points = [] #all the points of the snake
        self.lengths = [] #distances between each point
        self.currentLength = 0 #total length of the snake
        self.allowedLength = 150 # total allowed Length 
        self.previousHead = 0 , 0 #previous headPoint of the snake
        
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood ,self.wFood, _ = self.imgFood.shape
        
        self.foodPoint = 0 , 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False
    #random food location at different positionS
    def randomFoodLocation(self):
        self.foodPoint = random.randint(100,1000),random.randint(100,600)
        
    
    
    
    
    #method for updating
    def update(self,imgMain,currentHead):
        #it doesnt run all the code make sure of that after the game ends
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300 , 400], 
                               scale = 7 , thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f"Your Score : {self.score}", [300, 400],
                               scale=7, thickness=5, offset=20)
        
        
        
        
        else: 
            #setting the head and putting up in the length and updating the length
            previous_x,previous_y = self.previousHead
            current_x, current_y = currentHead
            #distance between current head and previous head points
            
            self.points.append([current_x,current_y])
            #finding the distance using hypotenuse function
            distance = math.hypot(current_x-previous_x,current_y-previous_y)
            self.lengths.append(distance)
            self.currentLength += distance
            #update the previous headpoint
            self.previousHead = current_x, current_y
            
            
            #Length Reduction Process in the snake
            if self.currentLength > self.allowedLength:
                for i , length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    
                    
                    if self.currentLength < self.allowedLength:
                        break 
            #check if snake eat the food
            random_x, random_y = self.foodPoint
            if random_x - self.wFood // 2 < current_x < random_x + self.wFood // 2 and random_y - self.hFood < current_y < random_y + self.hFood:
                # print("Ate the food")
                
                self.randomFoodLocation()
                self.allowedLength += 50
                
                self.score += 1
                print(self.score)

            
            #Drawing Snake  on the frame
            if self.points:
                for i,point in enumerate(self.points):
                    if i != 0 :
                        cv2.line(imgMain,self.points[i-1], self.points[i],(0,0,255),20)
                cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED)
            
            #Drawing Food
            random_x,random_y = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (random_x - self.wFood // 2 , random_y - self.hFood // 2)) 
            
            cvzone.putTextRect(imgMain, f" Score : {self.score}", [50, 80],
                            scale = 3, thickness=3, offset=10)
            

    #Check for collision of the snake with his body (its a tricky one)

            #create an array of polygon-points
            points = np.array(self.points[:-2], np.int32)
            points = points.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [points], False, (0, 200, 0), 3)
            #check whether this head point is colliding or not 
            minimumDistance = cv2.pointPolygonTest(points,(current_x,current_y),True)
            print (minimumDistance)
            
            #check whether point is hitting or not
            
            if -1 <= minimumDistance <= 1:
                print("Hitting the point")
                self.gameOver = True
                self.points = []  # all the points of the snake
                self.lengths = []  # distances between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous headPoint of the snake
                self.score = 0
                self.randomFoodLocation()
        
        
        return imgMain

#draw the frame and update the methods
game = SnakeGameClass("./images/donut.png ")
               








while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img,flipType = False)
    
    # creating a landmark of index finger as a point
    #created a dictionary of landmarkList which will be a relevant for index finger which is 8
    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        # cv2.circle(img,pointIndex,20,(200,0,200),cv2.FILLED)
        img = game.update(img,pointIndex)

    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
    


    
