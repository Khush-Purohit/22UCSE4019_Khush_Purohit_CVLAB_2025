import cv2
import numpy as np
from matplotlib import pyplot as plt

def detect_edges(image_path):
    # Read the medical image
    img = cv2.imread(image_path, 0)  
    
    if img is None:
        raise ValueError("Image could not be loaded. Check the file path.")
    
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_combined = np.sqrt(sobelx**2 + sobely**2)
    sobel_combined = np.uint8(sobel_combined)
    
    
    canny = cv2.Canny(blurred, 50, 150)
    
    
    plt.figure(figsize=(15, 5))
    
    plt.subplot(131), plt.imshow(img, cmap='gray')
    plt.title('Original Image'), plt.axis('off')
    
    plt.subplot(132), plt.imshow(sobel_combined, cmap='gray')
    plt.title('Sobel Edge Detection'), plt.axis('off')
    
    plt.subplot(133), plt.imshow(canny, cmap='gray')
    plt.title('Canny Edge Detection'), plt.axis('off')
    
    plt.tight_layout()
    plt.show()

try:
    detect_edges("brain_tumer_image.png")
except Exception as e:
    print(f"Error: {str(e)}")