from tkinter import ttk
import cv2
import tkinter as tk
from tkinter import Scale, HORIZONTAL
from PIL import Image, ImageTk
import numpy as np

contrast = 100
brightness = 0
hue = 0
sharpness = 1.0

def update_contrast(val):
    """Update the contrast value from the slider."""
    global contrast
    contrast = int(val)

def update_brightness(val):
    """Update the brightness value from the slider."""
    global brightness
    brightness = int(val)

def update_hue(val):
    """Update the hue value from the slider."""
    global hue
    hue = int(val)

def update_sharpness(val):
    """Update the sharpness value from the slider."""
    global sharpness
    sharpness = float(val)

def apply_hue(frame, hue_value):
    """Apply hue adjustment to the frame."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV
    hsv_frame[:, :, 0] = (hsv_frame[:, :, 0] + hue_value) % 180  # Adjust hue
    return cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)  # Convert back to BGR

def apply_sharpness(frame, sharpness_value):
    """Apply sharpness adjustment using a kernel."""
    kernel = np.array([[0, -1, 0], [-1, 5+sharpness_value, -1], [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)

def update_frame():
    """Capture frame, apply adjustments, and update the Tkinter window."""
    global contrast, brightness, hue, sharpness, cap, video_label

    # Capture frame from the webcam
    ret, frame = cap.read()
    if ret:
        # Apply contrast and brightness adjustments
        alpha = contrast / 100  # Scale contrast (0.5 to 3.0)
        beta = brightness       # Adjust brightness (-100 to 100)
        adjusted_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        # Apply hue adjustment
        adjusted_frame = apply_hue(adjusted_frame, hue)

        # Apply sharpness adjustment
        adjusted_frame = apply_sharpness(adjusted_frame, sharpness)

        # Convert BGR (OpenCV format) to RGB (Tkinter compatible)
        rgb_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Schedule the next update
    video_label.after(10, update_frame)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

# Set default resolution for the webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create the main Tkinter window
window = tk.Tk()
window.geometry("900x650")
window.title("Webcam Adjustments: Contrast, Brightness, Hue, Sharpness")

# Create a label to display the video feed
video_label = tk.Label(window)
video_label.pack()

# Contrast slider
contrast_slider = Scale(
    window,
    from_=50, to=200,  # Contrast range (0.5 to 2.0)
    orient=HORIZONTAL,
    label="Contrast",
    command=update_contrast
)
contrast_slider.set(100)  # Default contrast value
contrast_slider.place(x=100, y=500)

# Brightness slider
brightness_slider = Scale(
    window,
    from_=-100, to=100,  # Brightness range (-100 to 100)
    orient=HORIZONTAL,
    label="Brightness",
    command=update_brightness
)
brightness_slider.set(0)  # Default brightness value
brightness_slider.place(x=300, y=500)

# Hue slider
hue_slider = Scale(
    window,
    from_=-90, to=90,  # Hue range (-90 to 90 degrees)
    orient=HORIZONTAL,
    label="Hue",
    command=update_hue
)
hue_slider.set(0)  # Default hue value
hue_slider.place(x=500, y=500)

# Sharpness slider
sharpness_slider = Scale(
    window,
    from_=0, to=5,  # Sharpness range (0 to 5)
    orient=HORIZONTAL,
    label="Sharpness",
    command=update_sharpness
)
sharpness_slider.set(1)  # Default sharpness value
sharpness_slider.place(x=700, y=500)

close_button = ttk.Button(window, text="CLOSE", command=window.destroy)
close_button.place(x=450, y=600)

# Start the video update loop
update_frame()

# Run the Tkinter main loop
window.mainloop()

# Release the webcam and destroy all OpenCV windows when done
cap.release()
cv2.destroyAllWindows()