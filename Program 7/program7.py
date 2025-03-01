import cv2
import numpy as np

def detect_shapes(image_path):
   
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)  
        
        vertices = len(approx)
        x, y, w, h = cv2.boundingRect(approx)
        
        area = cv2.contourArea(contour)
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        if vertices == 3:
            shape = "Triangle"
        elif vertices == 4:
            
            angles = []
            for i in range(4):
                pt1 = tuple(approx[i][0])
                pt2 = tuple(approx[(i+1) % 4][0])
                pt3 = tuple(approx[(i+2) % 4][0])
                
                v1 = (pt1[0] - pt2[0], pt1[1] - pt2[1])
                v2 = (pt3[0] - pt2[0], pt3[1] - pt2[1])
                
                dot_product = v1[0] * v2[0] + v1[1] * v2[1]
                mag1 = np.sqrt(v1[0]**2 + v1[1]**2)
                mag2 = np.sqrt(v2[0]**2 + v2[1]**2)
                
                cos_angle = dot_product / (mag1 * mag2)
                angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))
                angles.append(angle)
            
            is_rectangular = all(abs(angle - 90) < 15 for angle in angles)  
            aspect_ratio = float(w)/h
            
            if is_rectangular and 0.90 <= aspect_ratio <= 1.10: 
                shape = "Square"
            elif is_rectangular:
                shape = "Rectangle"
            else:
                shape = "Unknown"
        elif circularity > 0.85:
            shape = "Circle"
        else:
            shape = "Unknown"

        cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)
        cv2.putText(image, shape, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Shapes Detected", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = "shape.png" 
detect_shapes(image_path)