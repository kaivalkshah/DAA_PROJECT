
import turtle

myPen = turtle.Turtle()
myPen._tracer(0)
myPen.speed(0)
myPen.color("#000000")
topLeft_x=-150
topLeft_y=150
colors = ["#DDDDDD","#888888","red","yellow","blue","green","orange","magenta","purple","brown","darkgreen","gold","skyblue","darkred","turquoise","cyan","navy","lightgreen"]

##### Setting up the game...
#Then let's have a list of all car (length, row, column, horizontal?, color)
cars = []
#Red Car:
cars.append([2,3,2,True,2]) 
#Yellow Car:
cars.append([3,1,4,False,3]) 
#Blue Car:
cars.append([3,2,5,False,4]) 
#Green Car:
cars.append([2,1,1,True,5]) 
#Orange Car:
cars.append([2,1,6,False,6]) 
#Magenta Car:
cars.append([2,5,1,False,7]) 
#Purple Car:
cars.append([3,2,1,False,8]) 
#Brown Car:
cars.append([2,3,6,False,9]) 
#Dark Green Car:
cars.append([3,4,2,True,10]) 
#Gold Car
cars.append([2,5,5,True,11]) 
#Cyan Car
cars.append([2,6,5,True,12]) 


#Try Another Puzzle:
#cars = []
#Red Car:
#cars.append([2,3,4,True,2]) 
#Other Cars (Yellow, Blue, Green...)
#cars.append([3,2,6,False,3]) 
#cars.append([2,1,5,False,4]) 
#cars.append([2,1,1,True,5]) 
#cars.append([2,1,3,True,6]) 
#cars.append([2,2,3,False,7]) 
#cars.append([2,3,2,False,8]) 
#cars.append([3,4,1,False,9]) 
#cars.append([2,4,4,True,10]) 
#cars.append([2,6,2,True,11]) 
#cars.append([2,6,5,True,12]) 
#cars.append([2,5,5,True,13]) 
#cars.append([2,5,4,False,14]) 

#A procedure to draw the ark/grid using Python Turtle
def drawGrid(width):
  for i in range(0,8):
    myPen.penup()
    myPen.goto(topLeft_x,topLeft_y-i*width)
    myPen.pendown()
    myPen.goto(topLeft_x+8*width,topLeft_y-i*width)
  for i in range(0,8):
    myPen.penup()
    myPen.goto(topLeft_x+i*width,topLeft_y)
    myPen.pendown()
    myPen.goto(topLeft_x+i*width,topLeft_y-8*width)
  for i in range(0,8):
    myPen.penup()
    myPen.goto(topLeft_x+i*width+10,topLeft_y+10)
    myPen.write(chr(65+i))
  for i in range(0,8):
    myPen.penup()
    myPen.goto(topLeft_x-15,topLeft_y-i*width+10-width)
    myPen.write(str(i)) 

  myPen.setheading(0)
  myPen.goto(topLeft_x,topLeft_y-width)
  for row in range (0,8):
      for column in range (0,8):
        if grid[row][column]>=0:
          square(width,grid[row][column])
        elif grid[row][column]==-1:
          square(width,0)
          
        myPen.penup()
        myPen.forward(width)
        myPen.pendown()	
      myPen.setheading(270) 
      myPen.penup()
      myPen.forward(width)
      myPen.setheading(180) 
      myPen.forward(width*8)
      myPen.setheading(0)
      myPen.pendown()

# This procedure draws a box by drawing each side of the square and using the fill function
def square(width,index):
    myPen.fillcolor(colors[index])
    myPen.begin_fill()
    for i in range(0,4):
      myPen.forward(width)
      myPen.left(90)
    myPen.end_fill()
    myPen.setheading(0)


#A Function to check if the grid is solved! (Red car next to the exit gate!)
def checkGrid(grid):
 if grid[3][6]==2:
    return True
 else:
    return False

grid=[]
grid    =  [[1,1,1,1,1,1,1,1]]
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,-1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,0,0,0,0,0,0,1])
grid.append([1,1,1,1,1,1,1,1])  
index=2
for car in cars:
  if car[3]==True:
    for i in range(0,car[0]):
      grid[car[1]][car[2]+i]=car[4]
  else:
    for i in range(0,car[0]):
      grid[car[1]+i][car[2]]=car[4]
  index+=1
drawGrid(30) #30 is the width of each square on the grid
myPen.getscreen().update()  

def stampGrid(grid):
  stamp = ""
  for row in range (1,7):
    for column in range (1,7):
      stamp = stamp + str(grid[row][column])
  return stamp
  
#Some moves will put the grid back into a position that has already been checked. If that's the case, there is no need to reinvestigate this position, we can backtrack!
history = []

def sendToFront(cars, color):
  index = 0
  for car in cars:
    if car[4]==color:
      cars.insert(0, cars.pop(index))
      break    
    index+=1
    
def sendToBack(cars, color):
  index = 0
  for car in cars:
    if car[4]==color:
      cars.append(cars.pop(index))
      break    
    index+=1
  
def applyHeuristics(grid,cars):
  #Priority 3 (Low): Vertical Cars in the way...
  for car in cars:
    if car[3]==False and grid[3][car[2]]==car[4]:
      sendToFront(cars,car[4])

  #Priority 2 (Medium): Horizontal Cars that can move to the left  
  for car in cars:
    if car[3]==True and car[4]!=2:
      if grid[car[1]][car[2]-1]==0:
        sendToFront(cars,car[4])
      else:  
        sendToBack(cars,car[4])

  #Priority 1 (High): Red car if it can move to the right  
  if (grid[3][2]==2 and grid[3][3]==0) or (grid[3][3]==2 and grid[3][4]==0) or (grid[3][4]==2 and grid[3][5]==0) or (grid[3][5]==2 and grid[3][6]==0):
    #Move Red Car to the Front of the queue
    sendToFront(cars,2)
  else:
    #Move Red Car to the Back of the queue
    sendToBack(cars,2)
    
#A recursive/backtracking function to check all possible positions for all pieces and discard positions that will not lead to a solution
def moveCars(grid,cars):
    stamp = stampGrid(grid)
    if stamp in history:
      return False
    else:
      history.append(stamp)
      
    applyHeuristics(grid,cars)
    for car in cars:
        color = grid[car[1]][car[2]]
        if car[3]==True: #horizontal car
          if color==2: #Red Car Heuristic - Try moving right first
            if grid[car[1]][car[2]+car[0]]==0:
              #Move right?
              grid[car[1]][car[2]+car[0]]=color
              grid[car[1]][car[2]]=0
              car[2]+=1
              if moveCars(grid,cars)==True:
                return True
              
              #Cancel move
              car[2]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]][car[2]+car[0]]=0
              
            if grid[car[1]][car[2]-1]==0:
              #Move left?
              grid[car[1]][car[2]+car[0]-1]=0
              grid[car[1]][car[2]-1]=color
              car[2]-=1
              if moveCars(grid,cars)==True:
                return True
              #Cancel move
              car[2]+=1
              grid[car[1]][car[2]+car[0]-1]=color
              grid[car[1]][car[2]-1]=0
          else: #All other horizontal cars: try moving left first
            if grid[car[1]][car[2]-1]==0:
              #Move left?
              grid[car[1]][car[2]+car[0]-1]=0
              grid[car[1]][car[2]-1]=color
              car[2]-=1
              if moveCars(grid,cars)==True:
                return True
              #Cancel move
              car[2]+=1
              grid[car[1]][car[2]+car[0]-1]=color
              grid[car[1]][car[2]-1]=0
              
            if grid[car[1]][car[2]+car[0]]==0:
              #Move right?
              grid[car[1]][car[2]]=0
              grid[car[1]][car[2]+car[0]]=color
              car[2]+=1
              if moveCars(grid,cars)==True:
                return True
              
              #Cancel move
              car[2]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]][car[2]+car[0]]=0  
            
        else: #Vertical cars...
          #Heurisitic: Trucks (size 3) to move down first, whereas cars (size 2) will go up
          if car[0]==3: #Trucks
            if grid[car[1]+car[0]][car[2]]==0:
              #Move down?
              grid[car[1]][car[2]]=0
              grid[car[1]+car[0]][car[2]]=color
              car[1]+=1
              if moveCars(grid,cars)==True:
                return True
              #Cancel move              
              car[1]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]+car[0]][car[2]]=0
              
            if grid[car[1]-1][car[2]]==0:
              #Move up?
              grid[car[1]+car[0]-1][car[2]]=0
              grid[car[1]-1][car[2]]=color
              car[1]-=1
              if moveCars(grid,cars)==True:
                return True  
              #Cancel move              
              car[1]+=1
              grid[car[1]+car[0]-1][car[2]]=color
              grid[car[1]-1][car[2]]=0
          else:
            if grid[car[1]-1][car[2]]==0:
              #Move up?
              grid[car[1]+car[0]-1][car[2]]=0
              grid[car[1]-1][car[2]]=color
              car[1]-=1
              if moveCars(grid,cars)==True:
                return True  
              #Cancel move              
              car[1]+=1
              grid[car[1]+car[0]-1][car[2]]=color
              grid[car[1]-1][car[2]]=0
            
            if grid[car[1]+car[0]][car[2]]==0:
              #Move down?
              grid[car[1]][car[2]]=0
              grid[car[1]+car[0]][car[2]]=color
              car[1]+=1
              if moveCars(grid,cars)==True:
                return True
              #Cancel move              
              car[1]-=1
              grid[car[1]][car[2]]=color
              grid[car[1]+car[0]][car[2]]=0
            
        drawGrid(30) #30 is the width of each square on the grid
        myPen.getscreen().update()  
        if checkGrid(grid):
          grid[3][5]=0
          grid[3][7]=2
          drawGrid(30) #30 is the width of each square on the grid
          myPen.getscreen().update()
          print("We have a solution!")
          return True
    return False
  
#Let's start the backtracking algorithm!
if moveCars(grid,cars):
  print("Problem Solved!")
else:
  print("This problem cannot be solved!")