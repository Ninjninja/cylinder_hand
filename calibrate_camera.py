import cv2
import pickle
import numpy as np
frames = []
coordinates = []

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY, coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv2.circle(img,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y
        print(mouseX, mouseY)
        coordinates.append([mouseX,mouseY])
    if event == cv2.EVENT_RBUTTONDOWN:
        # cv2.circle(img,(x,y),100,(255,0,0),-1)
        print('reset')
        coordinates = []


# img = np.zeros((512,512,3), np.uint8)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
frames = np.load('2D_coordinates.npy')
for i in range(11,12):
    img = cv2.imread('../datasets/data3_hand/img_'+str(i).zfill(4)+'.png')
    cv2.imshow('image',img)
    k = cv2.waitKey()
    frames[i] = np.array(coordinates)
    # frames.append(np.array(coordinates))
    coordinates = []
# print(frames)
np.save('2D_coordinates2.npy', np.array(frames))
# cv2.imshow('img', img)
# cv2.waitKey()
