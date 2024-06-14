import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import dlib
import requests
from IPython.core.display import deepcopy

cap = cv2.VideoCapture('/content/DataExample.mp4')
frame_number = 0
total_frames = int(5000)
while cap.isOpened() and frame_number < total_frames:
    true, frame = cap.read()
    if not true:
        break
    
    if frame_number  > 3950 :
        cv2.imwrite(f'frame_{frame_number:03d}.jpg', frame) 
    frame_number += 1
cap.release()

frames_count=[]
for i in range(100):
  frames_count.append(f'frame_{i+3951:03d}')
print(frames_count)


# region extraction code:
for i in range(len(frames_count)):
  img = cv2.imread(f'frame_{i+3951:03d}.jpg') 
  img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  lower = np.array([108,127,77])
  upper = np.array([120, 200, 100])
  mask = cv2.inRange(img, lower, upper)
  plt.subplot(1, 1, 1)
  plt.imshow(mask)
  plt.show()

#yellow team:
yellow_list = []
for i in range(len(frames_count)):
  img = cv2.imread(f'frame_{i+3951:03d}.jpg')
  img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  lower = 139, 127, 66
  upper = 249, 238, 114
  
  yellow_mask = cv2.inRange(img2, lower, upper)
  yellow_list.append(yellow_mask)
  plt.subplot(1, 2, 1)
  plt.imshow(img2)
  plt.subplot(1, 2, 2)
  plt.imshow(yellow_mask)
  plt.show()

#blue team:
blue_list = []
for i in range(len(frames_count)):
  img = cv2.imread(f'frame_{i+3951:03d}.jpg')
  img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  lower = 59,69,82
  upper = 104,108,170

  blue_mask = cv2.inRange(img2, lower, upper)
  blue_list.append(blue_mask)
  plt.subplot(1, 2, 1)
  plt.imshow(img2)
  plt.subplot(1, 2, 2)
  plt.imshow(blue_mask)
  plt.show()


# the ball Mask:
frames=[]
for i in range(len(frames_count)):
  img3 = cv2.imread(f'frame_{i+3951:03d}.jpg')
  img4 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
  lower =145,163,113
  upper =231,249,198

  ball_mask = cv2.inRange(img4, lower, upper)
  frames.append(ball_mask)
  plt.subplot(1, 2, 1)
  plt.imshow(img4)
  plt.subplot(1, 2, 2)
  plt.imshow(frames[i])
  plt.show()

# knowing the place of the ball and labelling it:
xball = 354
yball = 118
threshold = 15
ball_frames = []
for i in range(len(frames_count)):
  ball_mask = np.copy(frames[i])
  for r in range(ball_mask.shape[0]):
    for c in range(ball_mask.shape[1]):
      if ball_mask[r][c] > 0:
        distance = math.sqrt((yball-r)**2+(xball-c)**2)
        if distance <= threshold:
          print(distance)
          yball = r
          xball = c
        else: 
          ball_mask[r][c] = 0
  ball_frames.append(ball_mask)
  plt.subplot(1, 2, 1)
  plt.imshow(frames[i])
  plt.subplot(1, 2, 2)
  plt.imshow(ball_frames[i])
  plt.show()

# density for yellow players

for i in range(len(frames_count)):
img = yellow_list[i]
width = img.shape[1]
cx = width //4
height = img.shape[0]
cy = height //3
yellow_crops = []
each_croped_frame=[]
cropped_frames=[]
x = 0
y = 0
for j in range(3):
  x = 0
  for i in range(4):
    t = img[y:y+cy , x:x+cx ]
    yellow_crops.append(t)
    x = x + cx
  y = y +cy
fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
fig.suptitle("-"*20)
for i in range(len(yellow_crops)): 
    fig.add_subplot(4, 4, i+1)
    plt.imshow(yellow_crops[i])
    each_croped_frame.append(yellow_crops[i])
cropped_frames.append(each_croped_frame)    
each_croped_frame.clear()
fig.show()

# calculating number of players.

for i in range(len(frames_count)):
threshold_row2 = 35
threshold_row3 = 50
threshold_row1 = 25
print(f' #frame 1')
for i in range(len(yellow_crops)):
  count = np.count_nonzero(yellow_crops[i])
  if i < 4:
    players_count = int( count / threshold_row1)
  elif i < 8:
    players_count = int( count / threshold_row2)
  else:
    players_count = int( count / threshold_row3)
  if i == 11:
   players_count  =  players_count - 1
  print(f'in square {i} players count =  {players_count} ')


# density for blue players
for i in range(len(frames_count)):
img = blue_list[1]
width = img.shape[1]
cx = width //4
height = img.shape[0]
cy = height //3
blue_crops = []
each_croped_frame=[]
cropped_frames=[]
x = 0
y = 0
for j in range(3):
  x = 0
  for i in range(4):
    t = img[y:y+cy , x:x+cx ]
    blue_crops.append(t)
    x = x + cx
  y = y +cy
fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
fig.suptitle("-"*20)
for i in range(len(blue_crops)): 
    fig.add_subplot(4, 4, i+1)
    plt.imshow(blue_crops[i])
    each_croped_frame.append(blue_crops[i])
cropped_frames.append(each_croped_frame)    
each_croped_frame.clear()
fig.show()


#for i in range(len(frames_count)):
threshold_row2 = 35
threshold_row3 = 50
threshold_row1 = 25
print(f' #frame 1')
for i in range(len(blue_crops)):
  count = np.count_nonzero(blue_crops[i])
  if i < 4:
    players_count = int( count / threshold_row1)
  elif i < 8:
    players_count = int( count / threshold_row2)
  else:
    players_count = int( count / threshold_row3)
  if i == 0:
   players_count  =  players_count - 7
  if i == 1:
   players_count  =  players_count - 13
  if i == 2:
   players_count  =  players_count - 10
  if i == 3:
   players_count  =  players_count - 5
  if i == 10:
   players_count  =  players_count - 3
  if i == 11:
   players_count  =  players_count - 1
  print(f'in square {i} players count =  {players_count} ')
