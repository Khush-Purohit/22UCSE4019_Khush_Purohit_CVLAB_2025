import imageio
import numpy as np 
import math 

def scale_image(image, scale_x, scale_y):

    original_width = len(image[0])
    original_height = len(image)
    new_width = int(original_width * scale_x)
    new_height = int(original_height * scale_y)

    scaled_image = [[(0, 0, 0) for _ in range(new_width)] for _ in range(new_height)]  # Initialize with black pixels

    for y in range(new_height):
        for x in range(new_width):
            original_x = int(x / scale_x)  
            original_y = int(y / scale_y)

            # Handle boundary conditions
            original_x = min(original_x, original_width - 1)
            original_y = min(original_y, original_height - 1)

            scaled_image[y][x] = image[original_y][original_x]

    return scaled_image


def image_rotate(image, degree):
    
    rads = math.radians(degree)

    rot_img = np.uint8(np.zeros(image.shape))

    height = rot_img.shape[0]
    width  = rot_img.shape[1]

    midx,midy = (width//2, height//2)

    for i in range(rot_img.shape[0]):
        for j in range(rot_img.shape[1]):
            x= (i-midx)*math.cos(rads)+(j-midy)*math.sin(rads)
            y= -(i-midx)*math.sin(rads)+(j-midy)*math.cos(rads)

            x=round(x)+midx 
            y=round(y)+midy 

            if (x>=0 and y>=0 and x<image.shape[0] and  y<image.shape[1]):
                rot_img[i,j,:] = image[x,y,:]

    return rot_img



def flip_image(image):
    
    width = len(image[0])
    height = len(image)

    flipped_image = [[(0, 0, 0) for _ in range(width)] for _ in range(height)] # Black initialization

    for y in range(height):
        for x in range(width):
            flipped_image[y][x] = image[y][width - 1 - x]

    return flipped_image



#----------------image scaling----------------#
image = imageio.imread("program_1_image.jpg")

a = float(input("Enter the scaling factor for width: "))
b = float(input("Enter the scaling factor for height: "))

scaled_image_data = scale_image(image, a,b)  

imageio.imwrite("scaled_image.png", scaled_image_data)

print("\n image successfully scaled and saved\n")


#----------------image rotation----------------#
angle = float(input("Enter the rotating angle: "))

rotated_image = image_rotate(image, angle)

imageio.imwrite("rotated_image.png", rotated_image)

print("\n image successfully rotated and saved\n")


#----------------image flipping----------------#
flipped_image = flip_image(image)

imageio.imwrite("flipped_image.png", flipped_image)

print("\n image successfully flipped and saved\n")