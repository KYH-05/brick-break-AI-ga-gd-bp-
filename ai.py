#----------------------------------------------------------------------------
import pygame
import sys  
import random
from random import uniform
from pygame.locals import *
import numpy as np
import math
import time
#--------------------------------------------------------------
#기본설정
pygame.init() 
screenWidth=469 #469
screenHeight=600
screen = pygame.display.set_mode((screenWidth, screenHeight)) 
pygame.display.set_caption('bricks breaking') 
clock = pygame.time.Clock() 
pygame.key.set_repeat(1, 1) #key (지연시간,간격)
#--------------------------------------------------------------
#색 설정
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
#--------------------------------------------------------------
#변수설정
p_size=200
signal=0#공이 벽돌에 닿은 후라는걸 알려줌(공이 벽돌에 닿으면 1/input값 측정 되면 0으로 복구)
signal1=0#공이 paddle에 닿고 올라간다는 걸 알려줌 (paddle 위치를 초기화하라는 목적)
signal3=0 #공이 아래로 떨어지면 유전 알고리즘
signal5=0 #튕김변수
signal6=0
x = random.randint(10,459)
y = random.randint(300,400)
d_list=[[7.26,8.056,6],[-4.302,-2.662,-6]]
d_select=random.randint(0,2)
dx = d_list[0][d_select]*random.choice([-1,1])
dy = d_list[1][d_select]
#x=220 #220
#y=400
#dx=6
#dy=-6
Generation=0
runtime_list=[0  for i in range(0,p_size)]
moving=[0 for i in range(0,p_size)] 
runtime_max_list=[0,0,0]
input1=0
input2=0
input3=0
input4=[0 for i in range(0,p_size)]
first=4 #node개수
second=8
third=4
fourth=1
node_num=(first+second+third+fourth) #총 node개수
weight_num=(first*second+second*third+third*fourth) #총 가중치 개수
#--------------------------------------------------------------
#paddle설정
paddles=[]
padddles1=[]
paddleHeight = 10 #10
paddleWidth = 117.25 #75
paddleX = (screenWidth-paddleWidth) / 2
paddleY=screenHeight-100
for i in range(0,p_size):
  paddle = pygame.Rect(paddleX,paddleY,paddleWidth,paddleHeight)
  paddles.append(paddle)
paddles1=paddles.copy()
#--------------------------------------------------------------
#brick설정
bricks = []
bricks1 =[]
bricsWidth=35
brickHeight=10
for c in range(0,13):
  for r in range(0,5):
    brick = pygame.Rect(c*(36)+1 ,r*(11)+1 ,bricsWidth ,brickHeight)	
    bricks.append(brick)
bricks1=bricks.copy()
#--------------------------------------------------------------
#함수(game)
def drawBall():
  pygame.draw.circle(screen,(0, 190, 250),(x,y),7)
#--------------------------------------------------------------
def drawPaddle():
  for paddle in paddles:
    pygame.draw.rect(screen,(0,190,200),paddle)
#--------------------------------------------------------------
def draw():
  screen.fill(BLACK)
  drawBall()
#--------------------------------------------------------------
def drawbrick():
  for brick in bricks:
    pygame.draw.rect(screen,(0,190,250),brick)
#--------------------------------------------------------------
def input():
  global signal,input1,input2,input3,input4,dy,dx,signal6
  #if signal==1:
  input1=x
  input2=y
  input3=500-y
  for i in range(0,p_size):
    input4[i]=abs(paddles[i].x+(117.25/2)-x)
    
#--------------------------------------------------------------  
def reset_game():
  global bricks1, bricks, x, y, dx, dy,signal,signal1
  bricks=bricks1.copy()
  paddles=paddles1.copy()
  x = random.randint(10,459)
  y = random.randint(300,400)
  d_list=[[7.26,8.056,6],[-4.302,-2.662,-6]]
  d_select=random.randint(0,2)
  dx = d_list[0][d_select]*random.choice([-1,1])
  dy = d_list[1][d_select]
  #x=220
  #y=400
  #dx=6
  #dy=-6  
  signal=0
  #signal1=0
  moving=[0 for i in range(0,p_size)]
  #runtime_list=[0  for i in range(0,p_size)]
  input1=0
  input2=0  
  input3=0
  input4=[0 for i in range(0,p_size)]
  for i in range(0,p_size):
    paddles[i].x=175.875
    moving[i]=0
#-------------------------------------------------------------- 
#함수(genetic)
def initialize():  
  global d
  global d_n
  d_n=[]
  d_n=[[(random.uniform(0,5)) for k in range(0,weight_num)] for i in range(0,p_size)]
  #지역 최적해
#--------------------------------------------------------------
def node_making():           
  global input1,input2,input3,input4,first,second,third,weight_num,node_num
  global node_set
  global d_n, outputs
  node_set=[]
  node_set=[[0 for i in range(0,node_num)] for k in range(0,p_size)]
  for i in range(0,p_size):
    node_set[i][0]=input1
    node_set[i][1]=input2
    node_set[i][2]=input3
    node_set[i][3]=input4[i]
  def ReLU(x):
    return np.maximum(0, x)
  def sigmoid(x):
    return 1/(1+np.exp(-x))  
  def softmax(X):
    exp_a = np.exp(X)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y  
  input=[] #node의 값
  hidden1=[]
  hidden2=[]
  ouput=[]
  outputs=[]#ouput node값들의 집합
  for a in range(0,p_size):
    
    input=[input1,input2,input3,input4[a]]
    
    w1=[[1 for i in range(0,second)] for k in range(0,first)]
    for i in range(0,first):
      for k in range(0,second):
        w1[i][k]=d_n[a][(i*second)+k]
        
    hidden1=np.dot(input,w1)
    hidden1=ReLU(hidden1)
    
    w2=[[1 for i in range(0,third)] for k in range(0,second)]
    for i in range(0,second):
      for k in range(0,third):
        w2[i][k]=d_n[a][(i*third+k)+first*second]
        
    hidden2=np.dot(hidden1,w2)
    hidden2=ReLU(hidden2)
    
    w3=[[1 for i in range(0,fourth)] for k in range(0,third)]
    for i in range(0,third):
      for k in range(0,fourth):
        w3[i][k]=d_n[a][(i*fourth+k)+first*second+second*third]    
       
    output=np.dot(hidden2,w3)
    ouput=np.tanh(output)
    outputs.append(output)
    output=[]
#--------------------------------------------------------------
def output():
  global node6,node7,moving,signal2,signal1,output_nodes
  moving=[0 for i in range(0,p_size)]
  for i in range(0,p_size): 
    if outputs[i]>=1:
      moving[i]=10
    elif outputs[i]<-1:
      moving[i]=-10
    elif -1<outputs[i]<1:
      moving[i]=0
#--------------------------------------------------------------
def runtime_plus():
  global runtime_list,d_n
  for i in range(0,p_size): 
    d_n[i].append(runtime_list[i])
  d_n.sort(key=lambda x : x[-1])
  runtime_list=[0 for i in range(0,p_size)]
#--------------------------------------------------------------
def selection():                                       
  global select_n,d_n
  select_n=[]
  for i in range(0,round(p_size/2)):
    select=[]
    select_n.append(select)
  #print(d_n)
  for i in range(0,round(p_size/2)):
    select_n[i]=d_n[(i+1)*-1]
  for i in range(0,round(p_size/2)):
    del select_n[i][-1]
#--------------------------------------------------------------
def crossover():
  global cross
  global cross_n
  cross_n=[]
  for i in range(0,round(p_size/2)):
    cross=[]
    cross_n.append(cross)
  for i in range(0,round(p_size/2)):
    cross_choice1=random.randint(0,3)
    cross_choice2=random.randint(0,3)
    for k in range(0,weight_num): 
      gen_choice=random.randint(0,1)
      if gen_choice==0:
        cross_n[i].append(select_n[cross_choice1][k])
      elif gen_choice==1:
        cross_n[i].append(select_n[cross_choice2][k])
#--------------------------------------------------------------  
def mutation():
  global select_n
  global cross_n
  global gK
  mut_per=80
  gK=0
  stack=(runtime_max_list[-1]+runtime_max_list[-2]+runtime_max_list[-2])/3
  if 0<=stack<6:
    gK=2
  elif 6<stack<12: 
    gK=1
  elif 12<=stack<18:
    gK=0.5
  elif 18<=stack<24:
    gk=0.1
  elif 24<=stack:
    gK=0.01
  each_mut_per=round(p_size*((100-mut_per)/2/100))
  
#-------------------------------------------------------------
  def gau(x,y):#스택 수가 쌓일수록 가우시안 정규 분포 값의 폭을 줄이기, select_one을 복제해서 가우시안 더하기
    return np.random.randn(x,y)*gK
  for b in range(each_mut_per,round(p_size/2)):
    select_n[b]=select_n[0].copy()
    for c in range(0,weight_num):
      select_n[b][c]=(select_n[b][c]+gau(1,1)[0][0])
  for b in range(each_mut_per,round(p_size/2)):
    cross_n[b]=select_n[0].copy()
    for c in range(0,weight_num):
      cross_n[b][c]=(select_n[b][c]+gau(1,1)[0][0])  
 #-------------------------------------------------------------  
def new_generation():
  global d_n
  global select_n,cross_n
  d_n=[]
  for i in range(0,round(p_size/2)):
    d_n.append(select_n[i])
  for i in range(0,round(p_size/2)):
    d_n.append(cross_n[i])
  select_n.clear()
  cross_n.clear()
#--------------------------------------------------------------
#초기화
initialize()
start=time.time()
#--------------------------------------------------------------
#게임실행 
while True:
#--------------------------------------------------------------
#종료
  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
#-------------------------------------------------------------- 
  #ball,paddle,brick 그리기
  draw()
  drawPaddle()
  drawbrick()
#--------------------------------------------------------------
  #공 이동
  x += dx
  y += dy
#--------------------------------------------------------------
  #좌우 벽 부딧히면 튕기기
  if x  > 469-7:
    if dx>0:
      dx=-dx
  if x  < 7:
    if dx<0:
      dx = -dx
#--------------------------------------------------------------
  #위 벽 부딧히면 튕기기
  if y  < 7:
    signal=1
    if dy<0:
      dy = -dy
#--------------------------------------------------------------
#아래
  if y>630:
    reset_game()
    signal3=1    
    Generation=Generation+1
    print("generation",Generation)
    Time=time.time()-start
    print("time:",Time)
    runtime_max_list.append(Time)
    print('max',max(runtime_max_list))
    start=time.time()
    for i in range(0,p_size):
      paddles[i].x=175.875
#--------------------------------------------------------------   
   #벽돌과 부딧히면 튕기고 벽돌 사라지기
  for b in bricks:
    if x > b.x and x < b.x+35 and y > b.y and y < b.y+10:
      if dy<0:
        dy = -dy
        signal=1
        bricks.remove(b)
#--------------------------------------------------------------  
  input()
  #print(input1,input2)
  node_making()
  output()
  if signal3==1:
    runtime_plus()
    selection()
    print(select_n[0])
    #print(select_n[1])
    #print(select_n[2])
    crossover()
    mutation()
    new_generation()
    signal3=0
#--------------------------------------------------------------
  #패드 이동
  for i in range(0,p_size): ###################
    if paddles[i].x!=2000:
      paddles[i].x=paddles[i].x+moving[i]
      if paddles[i].x<=0:
        paddles[i].x=0
      elif paddles[i].x>=(469-117.25):
        paddles[i].x=(469-117.25)
     
#--------------------------------------------------------------
  #paddle과 부딧히면튕기기 안부딧힌건 삭제
  signal5=0
  if(y + 7 > 500):
    for i in range(0,p_size): ###################
      if dy<0 and signal6==1:
        for i in range(0,p_size):
          if paddles[i].x!=2000:
            paddles[i].x=175.875
          moving[i]=0
        signla6=0
      if (x > paddles[i].x-10 and x<paddles[i].x+23.45) or (x >= paddles[i].x+93.8 and x<paddles[i].x+117.25+10):
        if dx<0:
          dx=-7.26
        elif dx>0:
          dx=7.26
        signal5=1
      elif (x >= paddles[i].x+23.45 and x<paddles[i].x+46.9)or (x >= paddles[i].x+70.35 and x<paddles[i].x+93.8): 
        if dx<0:
          dx=-8.056
        elif dx>0:
          dx=8.056
        signal5=2
      elif x >= paddles[i].x+46.9 and x<paddles[i].x+70.35:
        if dx<0:
          dx=-6
        elif dx>0:
          dx=6
        signal5=3
      else: #삭제하고 runtime list로
        if paddles[i].x!=2000:
          runtime_list[i]=time.time()-start #를 runtime 리스토로
          paddles[i].x=2000 
      if signal5==1 and i==(p_size-1):
        if dy>0:
          dy=-4.392
        signal5=0
        signal6=1
      elif signal5==2 and i==(p_size-1):
        if dy>0:
          dy=-2.662
        signal5=0
        signal6=1
      elif signal5==3 and i==(p_size-1):
        if dy>0:
          dy=-6
        signal5=0
        signal6=1
#--------------------------------------------------------------
#학습완료 인공신경망
#--------------------------------------------------------------
  pygame.display.update()
  clock.tick(60)
#--------------------------------------------------------------
