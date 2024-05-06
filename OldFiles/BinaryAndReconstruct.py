from PIL import Image
import random

im1 = Image.open("../testing/test.jpg")
im2 = Image.open('gruddling.jpg')
im_width, im_height = im1.size
im1.show("IM 1")

im2_width, im2_height = im2.size
im2.show("IMG 2")
#
# for i in range(im_width):
#     for j in range(im_height):
#         R = im1.getpixel((i, j))[0]
#         G = im1.getpixel((i, j))[1]
#         B = im1.getpixel((i, j))[2]
#
#         if random.randint(0, 1) == 1:
#             if R % 2 == 0:
#                 R += 1
#             if G % 2 == 0:
#                 G += 1
#             if B % 2 == 0:
#                 B += 1
#         else:
#             if R % 2 == 1:
#                 R -= 1
#             if G % 2 == 1:
#                 G -= 1
#             if B % 2 == 1:
#                 B -= 1
#         im1.putpixel((i, j), (R, G, B))
#
# im1.show()
#
# for i in range(im_width):
#     for j in range(im_height):
#         R = im1.getpixel((i, j))[0]
#         G = im1.getpixel((i, j))[1]
#         B = im1.getpixel((i, j))[2]
#         if(R%2==0 and G%2==0 and B%2==0):
#             im1.putpixel((i, j), (0,0,0))
#         elif(R%2==1 and G%2==1 and B%2==1):
#             im1.putpixel((i, j), (255,255,255))
#         else:
#             im1.putpixel((i, j), (255,0,210))
#             print("ERROR: "+str(i)+" " + str(j))
# im1.show()


binary_string = ''
for i in range(im_width):
    for j in range(im_height):
        r, g, b = im1.getpixel((i, j))
        # Convert each RGB value to binary and concatenate them
        binary_string += '{:08b}{:08b}{:08b}'.format(r, g, b)

print(binary_string)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=

reconstructed_image = Image.new("RGB", (im_width, im_height))

# Load pixel data
pixels = reconstructed_image.load()

# Iterate through the binary string and set pixel values
index = 0
for i in range(im_width):
    for j in range(im_height):
        # Extract RGB values from the binary string
        r = int(binary_string[index:index + 8], 2)
        g = int(binary_string[index + 8:index + 16], 2)
        b = int(binary_string[index + 16:index + 24], 2)
        index += 24  # Move index to the next pixel

        # Set pixel value in the reconstructed image
        pixels[i, j] = (r, g, b)

# Save the reconstructed image to a file
reconstructed_image.show()
