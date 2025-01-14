import cv2


camera = cv2.VideoCapture(0)

print("Press 'c' to capture an image and 'q' to quit.")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Failed to grab frame.")
        break

   
    cv2.imshow("Camera", frame)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Press 'c' to capture the image
       
        image_filename = "program_1_image.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
        

        height, width, _ = frame.shape
        num_pixels = height * width
        print(height, width)
        print(f"Number of pixels in the captured image: {num_pixels}")

    elif key == ord('q'):  # Press 'q' to quit
        print("Exiting...")
        break

camera.release()
cv2.destroyAllWindows()