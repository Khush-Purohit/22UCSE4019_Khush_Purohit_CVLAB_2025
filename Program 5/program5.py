import cv2
import matplotlib.pyplot as plt
import numpy as np

# Reading the image in color (remove the 0 flag)
img = cv2.imread('pikachu.jpeg')

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])
hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])


img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
img_equalized = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

img_equalized_rgb = cv2.cvtColor(img_equalized, cv2.COLOR_BGR2RGB)


hist_r_eq = cv2.calcHist([img_equalized], [2], None, [256], [0, 256])
hist_g_eq = cv2.calcHist([img_equalized], [1], None, [256], [0, 256])
hist_b_eq = cv2.calcHist([img_equalized], [0], None, [256], [0, 256])

plt.figure(figsize=(12, 8))


plt.subplot(221)
plt.imshow(img_rgb)
plt.title('Original Image')
plt.axis('off')

plt.subplot(222)
plt.plot(hist_r, color='red', label='Red')
plt.plot(hist_g, color='green', label='Green')
plt.plot(hist_b, color='blue', label='Blue')
plt.title('Original Histogram')
plt.xlim([0, 256])
plt.legend()

plt.subplot(223)
plt.imshow(img_equalized_rgb)
plt.title('Equalized Image')
plt.axis('off')

plt.subplot(224)
plt.plot(hist_r_eq, color='red', label='Red')
plt.plot(hist_g_eq, color='green', label='Green')
plt.plot(hist_b_eq, color='blue', label='Blue')
plt.title('Equalized Histogram')
plt.xlim([0, 256])
plt.legend()

plt.tight_layout()
plt.show()

# Save the equalized image
cv2.imwrite('equalized_image.jpg', img_equalized)