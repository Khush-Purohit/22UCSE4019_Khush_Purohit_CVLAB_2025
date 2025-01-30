import cv2
import numpy as np
from matplotlib import pyplot as plt

def apply_low_pass_filter(img, cutoff):
    """Apply a Low Pass Filter in the Fourier domain."""
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2  

    mask = np.zeros((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), cutoff, 1, thickness=-1)

    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    dft_shift *= mask[:, :, np.newaxis]

    dft_ishift = np.fft.ifftshift(dft_shift)
    filtered_img = cv2.idft(dft_ishift)
    filtered_img = cv2.magnitude(filtered_img[:, :, 0], filtered_img[:, :, 1])

    return np.uint8(filtered_img / np.max(filtered_img) * 255)  


def apply_high_pass_filter(img, cutoff):
    """Apply a High Pass Filter in the Fourier domain."""
    rows, cols = img.shape
    crow, ccol = rows // 2, cols // 2 

    
    mask = np.ones((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), cutoff, 0, thickness=-1)

    
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    dft_shift *= mask[:, :, np.newaxis]

   
    dft_ishift = np.fft.ifftshift(dft_shift)
    filtered_img = cv2.idft(dft_ishift)
    filtered_img = cv2.magnitude(filtered_img[:, :, 0], filtered_img[:, :, 1])

    return np.uint8(filtered_img / np.max(filtered_img) * 255)



image_path = "pikachu.jpeg"
original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

low_pass_result = apply_low_pass_filter(original_img, cutoff=30)


high_pass_result = apply_high_pass_filter(original_img, cutoff=30)


cv2.imwrite("low_pass_filtered.jpg", low_pass_result)
cv2.imwrite("high_pass_filtered.jpg", high_pass_result)

# Displaying the results
plt.figure(figsize=(10, 8))
plt.subplot(1, 3, 1), plt.title("Original Image"), plt.imshow(original_img, cmap="gray"), plt.axis("off")
plt.subplot(1, 3, 2), plt.title("Low Pass Filtered"), plt.imshow(low_pass_result, cmap="gray"), plt.axis("off")
plt.subplot(1, 3, 3), plt.title("High Pass Filtered"), plt.imshow(high_pass_result, cmap="gray"), plt.axis("off")
plt.tight_layout()
plt.show()
