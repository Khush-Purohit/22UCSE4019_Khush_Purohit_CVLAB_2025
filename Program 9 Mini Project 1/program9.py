import cv2
import numpy as np
import os

img = cv2.imread('image.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def get_y_coordinate(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return y

contours = sorted(contours, key=get_y_coordinate)

current_row = 0
prev_y = -1
row_threshold = 10  

if not os.path.exists('output'):
    os.makedirs('output')

for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    
    if prev_y == -1 or abs(y - prev_y) > row_threshold:
        current_row += 1
        row_dir = f'output/row_{current_row}'
        if not os.path.exists(row_dir):
            os.makedirs(row_dir)
    

    char_img = thresh[y:y+h, x:x+w]
    
 
    filename = f'{row_dir}/char_{i+1}.png'
    cv2.imwrite(filename, char_img)
    
    prev_y = y

print(f"Processing complete. Check the 'output' folder for results.")