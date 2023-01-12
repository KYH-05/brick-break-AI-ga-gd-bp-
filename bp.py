#1. 어떤 경우라도 기울기가 완만해지는가?-기울기가 너무 크면 너무 이동해서
#2. 기울기가 완만해질때 cost가 항상 작아지는가?
#3. 항상 전역 최적해 수렴이 보장되는가
#4. 전역 최적해가 기울기 0이라는 조건이 성립하는가?
# ----------------------------------------------------------------------------
import sys
import random
from random import uniform
import numpy as np
import math
import time
from sympy import symbols, diff
import pygame
# --------------------------------------------------------------
# 기본설정
pygame.init()
screenWidth = 469  # 469
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('bricks breaking')
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)  # key (지연시간,간격)
# --------------------------------------------------------------
# 색 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# --------------------------------------------------------------
# 변수설정
signal = 0  # 공이 벽돌에 닿은 후라는걸 알려줌(공이 벽돌에 닿으면 1/input값 측정 되면 0으로 복구)
signal1 = 0  # 공이 paddle에 닿고 올라간다는 걸 알려줌 (paddle 위치를 초기화하라는 목적)
signal3 = 0  # 공이 아래로 떨어지면 유전 알고리즘
signal5 = 0  # 튕김변수
signal6 = 0
#x = random.randint(10, 459)
#y = random.randint(300, 400)
#d_list = [[7.26, 8.056, 6], [-4.302, -2.662, -6]]
#d_select = random.randint(0, 2)
#dx = d_list[0][d_select] * random.choice([-1, 1])
#dy = d_list[1][d_select]
x=220 #220
y=400
dx=6
dy=-6
moving = 0
input1 = 0
input2 = 0
input3 = 0
input4 = 0
first = 4  # node개수
second = 8
third = 4
fourth = 1
node_num = (first + second + third + fourth)  # 총 node개수
weight_num = (first * second + second * third + third * fourth)  # 총 가중치 개수
gradient_start=0
stack=0
new_sig=0
# --------------------------------------------------------------
# paddle설정
paddles = []
padddles1 = []
paddleHeight = 10  # 10
paddleWidth = 117.25  # 75
paddleX = (screenWidth - paddleWidth) / 2
paddleY = screenHeight - 100
for i in range(0, 1):
    paddle = pygame.Rect(paddleX, paddleY, paddleWidth, paddleHeight)
    paddles.append(paddle)
paddles1 = paddles.copy()
# --------------------------------------------------------------
# brick설정
bricks = []
bricks1 = []
bricsWidth = 35
brickHeight = 10
for c in range(0, 13):
    for r in range(0, 5):
        brick = pygame.Rect(c * (36) + 1, r * (11) + 1, bricsWidth, brickHeight)
        bricks.append(brick)
bricks1 = bricks.copy()


# --------------------------------------------------------------
# 함수(game)
def drawBall():
    pygame.draw.circle(screen, (0, 190, 250), (x, y), 7)


# --------------------------------------------------------------
def drawPaddle():
    for paddle in paddles:
        pygame.draw.rect(screen, (0, 190, 200), paddle)


# --------------------------------------------------------------
def draw():
    screen.fill(BLACK)
    drawBall()


# --------------------------------------------------------------
def drawbrick():
    for brick in bricks:
        pygame.draw.rect(screen, (0, 190, 250), brick)


# --------------------------------------------------------------
def input():
    global signal, input1, input2, input3, input4, dy, dx, signal6
    # if signal==1:
    input1 = x
    input2 = y
    input3 = 500 - y
    input4 = abs(paddles[0].x + (117.25 / 2) - x)


# --------------------------------------------------------------
def reset_game():
    global bricks1, bricks, x, y, dx, dy, signal, signal1,stack
    bricks = bricks1.copy()
    paddles = paddles1.copy()
    #x = random.randint(10, 459)
    #y = random.randint(300, 400)
    #d_list = [[7.26, 8.056, 6], [-4.302, -2.662, -6]]
    #d_select = random.randint(0, 2)
    #dx = d_list[0][d_select] * random.choice([-1, 1])
    #dy = d_list[1][d_select]
    x=220
    y=400
    dx=6
    dy=-6
    signal = 0
    # signal1=0
    moving = 0
    # runtime_list=[0  for i in range(0,p_size)]
    input1 = 0
    input2 = 0
    input3 = 0
    input4 = 0
    stack=0

# --------------------------------------------------------------
# 함수(genetic)
def initialize():
    global d
    global d_n
    d_n = []
    d_n = [(random.uniform(-1.0, 1.0)) for k in range(0, weight_num)]
    # 지역 최적해
    d_n=[0.5586003233920689, 0.27815294071341845, -0.8361642283470694, -0.44349170422462336, -0.1023620263641487, 0.93194231391536, -0.40557587656476857, 0.539687517818465, 0.05108677942505957, -0.8018268926670242, -0.5562361038395378, -0.07587722232024996, 0.23853898219621938, -0.8220694596812739, -0.02814632389027194, -0.6649464454813829, 0.30591661016538185, 0.7482587604408901, -0.20985893410044443, -0.10490186891611297, 0.6931482620095848, -0.797043144765583, 0.25163094899128424, -0.24110056411312186, 0.5522955017036415, -0.018699554146241137, -0.22449785077463913, 0.781369518859075, -0.5412497338159916, 0.589295363180812, -0.11767803678309385, 0.872833691722323, 0.9939834357671751, -0.3877536872548497, 0.7517027096218374, 0.46277262542478104, 0.744564793308113, -0.1946784082948989, -0.3336240396503225, -0.4585434093669565, -0.39423823824876014, 0.5103774094109508, -0.03448086146413498, -0.664050556045463, 0.7321335901557486, 0.2904786727014679, 0.12954015084697912, -0.5058258326448992, -0.5196458011667051, -0.5567778075984313, 0.7473085677860807, -0.724109528917676, 0.6377792778818341, 0.4477385793275699, 0.8037533936329151, 0.8661247358885691, -0.4640732673320216, 0.6746082491008878, 0.06588828162197036, -0.8794966047136445, 0.10823693276088786, -0.08618103637353336, 0.6693067363903231, -0.5264991652419233, 0.25227969322239874, 0.006904489088324084, -0.3948828920166143, -0.2529323133671264]

    print(d_n)

    #for i in range(0,68):
     # n=random.sample([-0.1, 0.1], 1)
      #d_n[i]=d_n[i]+ n[0]
# --------------------------------------------------------------
def node_making():
    global input1, input2, input3, input4, first, second, third, weight_num, node_num
    global node_set
    global d_n, outputs
    i1=input1
    i2=input2
    i3=input3
    i4=input4
    w1 = d_n[0]
    w2 = d_n[1]
    w3 = d_n[2]
    w4 = d_n[3]
    w5 = d_n[4]
    w6 = d_n[5]
    w7 = d_n[6]
    w8 = d_n[7]
    w9 = d_n[8]
    w10 = d_n[9]
    w11 = d_n[10]
    w12 = d_n[11]
    w13 = d_n[12]
    w14 = d_n[13]
    w15 = d_n[14]
    w16 = d_n[15]
    w17 = d_n[16]
    w18 = d_n[17]
    w19 = d_n[18]
    w20 = d_n[19]
    w21 = d_n[20]
    w22 = d_n[21]
    w23 = d_n[22]
    w24 = d_n[23]
    w25 = d_n[24]
    w26 = d_n[25]
    w27 = d_n[26]
    w28 = d_n[27]
    w29 = d_n[28]
    w30 = d_n[29]
    w31 = d_n[30]
    w32 = d_n[31]
    w33 = d_n[32]
    w34 = d_n[33]
    w35 = d_n[34]
    w36 = d_n[35]
    w37 = d_n[36]
    w38 = d_n[37]
    w39 = d_n[38]
    w40 = d_n[39]
    w41 = d_n[40]
    w42 = d_n[41]
    w43 = d_n[42]
    w44 = d_n[43]
    w45 = d_n[44]
    w46 = d_n[45]
    w47 = d_n[46]
    w48 = d_n[47]
    w49 = d_n[48]
    w50 = d_n[49]
    w51 = d_n[50]
    w52 = d_n[51]
    w53 = d_n[52]
    w54 = d_n[53]
    w55 = d_n[54]
    w56 = d_n[55]
    w57 = d_n[56]
    w58 = d_n[57]
    w59 = d_n[58]
    w60 = d_n[59]
    w61 = d_n[60]
    w62 = d_n[61]
    w63 = d_n[62]
    w64 = d_n[63]
    w65 = d_n[64]
    w66 = d_n[65]
    w67 = d_n[66]
    w68 = d_n[67]
    outputs = w65 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w33 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w37 + w41 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w45 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w49 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w53 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w57 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w61 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32)) + w66 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w34 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w38 + w42 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w46 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w50 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w54 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w58 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w62 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32)) + w67 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w35 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w39 + w43 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w47 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w51 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w55 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w59 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w63 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32)) + w68 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w36 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w40 + w44 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w48 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w52 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w56 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w60 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w64 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32))
    #print(outputs)

# --------------------------------------------------------------
def output():
    global node6, node7, moving, signal2, signal1, outputs
    #moving = 0
    #if outputs<0:
      #moving=0
    #elif outputs>469:
      #moving=469
    #else:
    moving = outputs


# --------------------------------------------------------------
# 오차 역전파-chain rule(역전파하듯 미분해 가중치를 조정)
def back():
  global d_n,outputs,hidden1,hidden2,z1,z2
  gradient=[0 for i in range(0,68)]
  print()
  print(d_n)
  print(abs(paddles[0].x + (117.25 / 2) - x))
  print()
  for i in range(0,68):
    #------------
    w1 = d_n[0]
    w2 = d_n[1]
    w3 = d_n[2]
    w4 = d_n[3]
    w5 = d_n[4]
    w6 = d_n[5]
    w7 = d_n[6]
    w8 = d_n[7]
    w9 = d_n[8]
    w10 = d_n[9]
    w11 = d_n[10]
    w12 = d_n[11]
    w13 = d_n[12]
    w14 = d_n[13]
    w15 = d_n[14]
    w16 = d_n[15]
    w17 = d_n[16]
    w18 = d_n[17]
    w19 = d_n[18]
    w20 = d_n[19]
    w21 = d_n[20]
    w22 = d_n[21]
    w23 = d_n[22]
    w24 = d_n[23]
    w25 = d_n[24]
    w26 = d_n[25]
    w27 = d_n[26]
    w28 = d_n[27]
    w29 = d_n[28]
    w30 = d_n[29]
    w31 = d_n[30]
    w32 = d_n[31]
    w33 = d_n[32]
    w34 = d_n[33]
    w35 = d_n[34]
    w36 = d_n[35]
    w37 = d_n[36]
    w38 = d_n[37]
    w39 = d_n[38]
    w40 = d_n[39]
    w41 = d_n[40]
    w42 = d_n[41]
    w43 = d_n[42]
    w44 = d_n[43]
    w45 = d_n[44]
    w46 = d_n[45]
    w47 = d_n[46]
    w48 = d_n[47]
    w49 = d_n[48]
    w50 = d_n[49]
    w51 = d_n[50]
    w52 = d_n[51]
    w53 = d_n[52]
    w54 = d_n[53]
    w55 = d_n[54]
    w56 = d_n[55]
    w57 = d_n[56]
    w58 = d_n[57]
    w59 = d_n[58]
    w60 = d_n[59]
    w61 = d_n[60]
    w62 = d_n[61]
    w63 = d_n[62]
    w64 = d_n[63]
    w65 = d_n[64]
    w66 = d_n[65]
    w67 = d_n[66]
    w68 = d_n[67]
    #------------
    i1=x
    i2=y
    i3=500-y
    if i==0:
      i4=abs(paddles[0].x + (117.25 / 2) - x)
    ANN_funtion = w65 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w33 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w37 + w41 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w45 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w49 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w53 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w57 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w61 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32)) + w66 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w34 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w38 + w42 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w46 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w50 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w54 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w58 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w62 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32)) + w67 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w35 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w39 + w43 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w47 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w51 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w55 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w59 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w63 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32)) + w68 * (i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26 + w36 * (i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25) + w40 + w44 * (i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27) + w48 * (i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28) + w52 * (i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29) + w56 * (i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30) + w60 * (i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31) + w64 * (i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32))
    i4=abs(ANN_funtion + (117.25 / 2) - x)
    #------------
    n1 = x
    n2 = y
    n3 = 500 - y
    n4 = abs(paddles[0].x + (117.25 / 2) - x)
    n5 = i1 * w1 + i2 * w9 + i3 * w17 + i4 * w25
    n6 = i1 * w2 + i2 * w10 + i3 * w18 + i4 * w26
    n7 = i1 * w3 + i2 * w11 + i3 * w19 + i4 * w27
    n8 = i1 * w4 + i2 * w12 + i3 * w20 + i4 * w28
    n9 = i1 * w5 + i2 * w13 + i3 * w21 + i4 * w29
    n10 = i1 * w6 + i2 * w14 + i3 * w22 + i4 * w30
    n11 = i1 * w7 + i2 * w15 + i3 * w23 + i4 * w31
    n12 = i1 * w8 + i2 * w16 + i3 * w24 + i4 * w32
    n13 = n5 * w33 + n6 + w37 + n7 * w41 + n8 * w45 + n9 * w49 + n10 * w53 + n11 * w57 + n12 * w61
    n14 = n5 * w34 + n6 + w38 + n7 * w42 + n8 * w46 + n9 * w50 + n10 * w54 + n11 * w58 + n12 * w62
    n15 = n5 * w35 + n6 + w39 + n7 * w43 + n8 * w47 + n9 * w51 + n10 * w55 + n11 * w59 + n12 * w63
    n16 = n5 * w36 + n6 + w40 + n7 * w44 + n8 * w48 + n9 * w52 + n10 * w56 + n11 * w60 + n12 * w64
    n17 = n13 * w65 + n14 * w66 + n15 * w67 + n16 * w68
    ns = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17]
    # ------------
    if 0<=i<=3:
      gradient[-(i+1)]=2*(ns[-1]-ANN_funtion) * ns[-(i+2)]
    elif 4<=i<=35:
      Ts=[-6,-6,-6,-6,-7,-7,-7,-7,-8,-8,-8,-8,-9,-9,-9,-9,-10,-10,-10,-10,-11,-11,-11,-11,-12,-12,-12,-12,-13,-13,-13,-13]#node index
      gradient[-(i+1)]=2*(ns[-1]-ANN_funtion)*gradient[-((i%4)+1)]* ns[Ts[i-4]]
    elif 36<=i<=67:
      Ts2=[-14,-14,-14,-14,-14,-14,-14,-14,-13,-13,-13,-13,-13,-13,-13,-13,-12,-12,-12,-12,-12,-12,-12,-12,-11,-11,-11,-11,-11,-11,-11,-11]#node index2
      Ts3=[-5,-9,-13,-17,-21,-25,-29,-33,-5,-9,-13,-17,-21,-25,-29,-33,-5,-9,-13,-17,-21,-25,-29,-33,-5,-9,-13,-17,-21,-25,-29,-33]
      gradient[-(i + 1)]=2*(ns[-1]-ANN_funtion)*(gradient[-1]*gradient[(i-36)]+gradient[-2]*gradient[(i-36)-1]+gradient[-3]*gradient[(i-36)-2]+gradient[-4]*gradient[(i-36)-3])*ns[Ts2[i-36]]
    #------------
    b1 = 0.9
    b2 = 0.999
    v = 1 / (10 ** 8)
    s = 1 / (10 ** 8)
    v_ang = 0
    s_ang = 0
    rate = 0.001  # 학습률 조정 #SA 기법 0.001일때 대략적으로 수렴했음
    v = b1 * v + (1 - b1) * gradient[-(i+1)]
    s = b2 * s + (1 - b2) * ((gradient[-(i+1)]) ** 2)
    #v_ang = (v / (1 - (b1) ** (-(i+1) + (1 / 10) * 5)))
    #s_ang = (s / (1 - (b2) ** (-(i+1) + (1 / 10) * 5)))
    Q = (v / (s + (1 / 10) ** 8) ** (1 / 2))
    d_n[-(i+1)] = d_n[-(i+1)] - rate * Q  # v_ang,s_ang로
  gradient_start = time.time()









# --------------------------------------------------------------
# 초기화
initialize()
start = time.time()
# --------------------------------------------------------------
# 게임실행
while True:
    # --------------------------------------------------------------
    # 종료
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # --------------------------------------------------------------
    # ball,paddle,brick 그리기
    draw()
    drawPaddle()
    drawbrick()
    # --------------------------------------------------------------
    # 공 이동
    x += dx
    y += dy
    # --------------------------------------------------------------
    # 좌우 벽 부딧히면 튕기기
    if x > 469 - 7:
        if dx > 0:
            dx = -dx
    if x < 7:
        if dx < 0:
            dx = -dx
    # --------------------------------------------------------------
    # 위 벽 부딧히면 튕기기
    if y < 7:
        signal = 1
        if dy < 0:
            dy = -dy
    # --------------------------------------------------------------
    # 아래
    if y > 630:
        reset_game()
        signal3 = 1
        Time = time.time() - start
        #print("time:", Time)
        start = time.time()
        new_sig=0
    # --------------------------------------------------------------
    # 벽돌과 부딧히면 튕기고 벽돌 사라지기
    for b in bricks:
        if x > b.x and x < b.x + 35 and y > b.y and y < b.y + 10:
            if dy < 0:
                dy = -dy
                signal = 1
                bricks.remove(b)
    # --------------------------------------------------------------
    input()
    # print(input1,input2)
    node_making()
    output()
    if signal3 == 1:
        # 경사하강 코드

        # print(select_n[1])
        # print(select_n[2])

        signal3 = 0
    # --------------------------------------------------------------
    # 패드 이동
    if paddles[0].x != 2000:
        if moving <= -100000000:
          paddles[0].x = -100000000
        elif moving >= 100000000:
          paddles[0].x = 100000000
        else:
          if type(moving) == np.ndarray:
            #print(1)
            #print(moving)
            moving = np.asarray(moving, dtype=int)
            moving = moving.tolist()
            moving = sum(moving, [])
            # print(moving)
          paddles[0].x = round(moving)

    # --------------------------------------------------------------
    # paddle과 부딧히면튕기기 안부딧힌건 삭제
    signal5 = 0
    if (520>y + 7 > 500):
        #######################################
        if time.time()-gradient_start>1: #and stack<5:
          back()#p 닿고 올라가면 잠시 함수 실행하지 않기
        #if dy < 0 and signal6 == 1:
            #if paddles[0].x != 2000:
                #paddles[0].x = 175.875
            #moving = 0
            #signla6 = 0
        #if new_sig == 1:
          #continue
        if (x > paddles[0].x - 10 and x < paddles[0].x + 23.45) or (x >= paddles[0].x + 93.8 and x < paddles[0].x + 117.25 + 10):
            if dx < 0:
                dx = -7.26
            elif dx > 0:
                dx = 7.26
            signal5 = 1
            stack=stack+1
        elif (x >= paddles[0].x + 23.45 and x < paddles[0].x + 46.9) or (
                x >= paddles[0].x + 70.35 and x < paddles[0].x + 93.8):
            if dx < 0:
                dx = -8.056
            elif dx > 0:
                dx = 8.056
            signal5 = 2
            stack = stack + 1
        elif x >= paddles[0].x + 46.9 and x < paddles[0].x + 70.35:
            if dx < 0:
                dx = -6
            elif dx > 0:
                dx = 6
            signal5 = 3
            stack = stack + 1

        #else:  # 삭제하고 runtime list로
          #new_sig=1
        if signal5 == 1:
            if dy > 0:
                dy = -4.392
            signal5 = 0
            signal6 = 1
        elif signal5 == 2:
            if dy > 0:
                dy = -2.662
            signal5 = 0
            signal6 = 1
        elif signal5 == 3:
            if dy > 0:
                dy = -6
            signal5 = 0
            signal6 = 1
    # --------------------------------------------------------------
    # 학습완료 인공신경망
    # --------------------------------------------------------------
    #print(paddles[0].x)
    pygame.display.update()
    clock.tick(60)
# --------------------------------------------------------------