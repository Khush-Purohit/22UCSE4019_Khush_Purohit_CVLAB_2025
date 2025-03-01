import cv2
import numpy as np

def add_watermark(image, watermark_text):
    watermarked = image.copy()
    h, w = image.shape[:2]
    
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 2.0
    thickness = 2
    color = (0, 0, 255)  # BGR color (red)
    
    (text_w, text_h), _ = cv2.getTextSize(watermark_text, font, font_scale, thickness)
    x = (w - text_w) // 2
    y = (h + text_h) // 2
    
    cv2.putText(watermarked, watermark_text, (x, y), font, font_scale, color, thickness)
    return watermarked, (x, y, text_w, text_h)

def remove_watermark(image, watermark_region):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    x, y, w, h = watermark_region
    
    padding = 10
    mask[y-h-padding:y+padding, x-padding:x+w+padding] = 255
    radius = 3
    restored = cv2.inpaint(image, mask, radius, cv2.INPAINT_TELEA)
    return restored

def resize_image(image, width=None, height=None):
    h, w = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        aspect_ratio = height / h
        width = int(w * aspect_ratio)
    if height is None:
        aspect_ratio = width / w
        height = int(h * aspect_ratio)
    return cv2.resize(image, (width, height))



image = cv2.imread('pikachu.jpeg')

watermark_text = "MBM University"
watermarked_image, watermark_region = add_watermark(image, watermark_text)
restored_image = remove_watermark(watermarked_image, watermark_region)

display_width = 400
image = resize_image(image, width=display_width)
watermarked_image = resize_image(watermarked_image, width=display_width)
restored_image = resize_image(restored_image, width=display_width)

combined_image = np.hstack((image, watermarked_image, restored_image))
cv2.imshow('Results (Original | Watermarked | Restored)', combined_image)

cv2.imwrite('watermarked.jpg', watermarked_image)
cv2.imwrite('restored.jpg', restored_image)

cv2.waitKey(0)
cv2.destroyAllWindows()