from PIL import Image
import random


def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False


def decrypt_binary_from_image(image):  # get encoded binary string from image
    im_width, im_height = image.size
    binary_string = ""
    for i in range(im_width):
        for j in range(im_height):
            (r, g, b) = image.getpixel((i, j))
            if r % 2 == 1 and g % 2 == 1 and b % 2 == 1:
                binary_string += str(1)
            elif r % 2 == 0 and g % 2 == 0 and b % 2 == 0:
                binary_string += str(0)
    return binary_string


def decryptV2(image):
    im_width, im_height = image.size
    binary_string = ""
    for i in range(im_width):
        for j in range(im_height):
            for color in image.getpixel((i, j)):
                if is_even(color):
                    binary_string += str(0)
                else:
                    binary_string += str(1)
    return binary_string


def translate_image_to_binary(image):  # makes binary string from image
    binary_string = ''
    image_width, image_height = image.size
    for i in range(image_width):
        for j in range(image_height):
            r, g, b = image.getpixel((i, j))
            # Convert each RGB value to binary and concatenate them
            binary_string += '{:08b}{:08b}{:08b}'.format(r, g, b)

    return binary_string


def encodeV2(image, binary):  # adds binary to image
    pass


def encode_binary_in_image(image, binary):  # adds binary to image
    im_width, im_height = image.size
    counter = 0
    pixels = image.load()
    for i in range(im_width):
        for j in range(im_height):
            R, G, B = pixels[i, j]
            if counter < len(binary):
                if int(binary[counter]) == 1:  # 1 is all odds
                    # pixels[i, j] = (255, 255, 255)
                    if R % 2 == 0:
                        R += 1
                    if G % 2 == 0:
                        G += 1
                    if B % 2 == 0:
                        B += 1
                elif int(binary[counter]) == 0:  # 0 is all evens
                    # pixels[i, j] = (0, 0, 0)

                    if R % 2 == 1:
                        R -= 1
                    if G % 2 == 1:
                        G -= 1
                    if B % 2 == 1:
                        B -= 1
            # else:
            #     pixels[i, j] = (255, 0, 210)
            pixels[i, j] = (R, G, B)
            counter += 1
    return image


def encode_random_binary_in_image(image):  # adds binary to image
    im_width, im_height = image.size
    counter = 0
    for i in range(im_width):
        for j in range(im_height):
            R = image.getpixel((i, j))[0]
            G = image.getpixel((i, j))[1]
            B = image.getpixel((i, j))[2]

            if random.randint(0, 1) == 1:
                if R % 2 == 0:
                    R += 1
                if G % 2 == 0:
                    G += 1
                if B % 2 == 0:
                    B += 1
            else:
                if R % 2 == 1:
                    R -= 1
                if G % 2 == 1:
                    G -= 1
                if B % 2 == 1:
                    B -= 1
            image.putpixel((i, j), (R, G, B))
            counter += 1
    return image


def image_from_binary(image):  # Make black and white image from binary
    new_image = image
    im_width, im_height = image.size
    for i in range(im_width):
        for j in range(im_height):
            R = new_image.getpixel((i, j))[0]
            G = new_image.getpixel((i, j))[1]
            B = new_image.getpixel((i, j))[2]
            if R % 2 == 0 and G % 2 == 0 and B % 2 == 0:
                new_image.putpixel((i, j), (0, 0, 0))
                # print("Black")
            elif R % 2 == 1 and G % 2 == 1 and B % 2 == 1:
                new_image.putpixel((i, j), (255, 255, 255))
            else:
                new_image.putpixel((i, j), (255, 0, 210))
                # print("ERROR: " + str(i) + " " + str(j))
    return new_image


def reconstruct_image(im_width, im_height, binary_string):  # reuild an image from sizes and the binary string
    image = Image.new("RGB", (im_width, im_height))
    # Load pixel data
    pixels = image.load()

    # Iterate through the binary string and set pixel values
    index = 0

    for i in range(im_width):
        for j in range(im_height):
            if index + 24 < len(binary_string):
                # Extract RGB values from the binary string
                r = int(binary_string[index:index + 8], 2)
                g = int(binary_string[index + 8:index + 16], 2)
                b = int(binary_string[index + 16:index + 24], 2)
                index += 24  # Move index to the next pixel

                # Set pixel value in the reconstructed image
                pixels[i, j] = (r, g, b)

    # Save the reconstructed image to a file
    return image


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


im1 = Image.open("../testing/test.jpg")
im2 = Image.open('../testing/TestEncoded.jpg')

im2_width, im2_height = im2.size

binary = translate_image_to_binary(im2)

encoded = encode_binary_in_image(im1, binary)
encoded.show()

image_from_binary(encoded).show()
#
reconstruct_image(im2.size[0], im2.size[1], decrypt_binary_from_image(encoded)).show()

"""
Current problem is that you need the exact size in pixel of the secret image, and for this to work that
needs to be encoded in the larger image so you can send just the encoded image to someone
and it'll decrypt it. I dont know how to encode that size, but currently we could reserve 64 bits at the start
and 32 bits for width and 32 bits for height. 

COOL IDEA
take all rgb values and make it just one long thing, so instead a 1 or 0 being stored in a single pixel,
its stored in an R value, or a G value, or a B value. So if odds are ones, and evens are 0s, then the string
"001011" could be encoded as (200,140,255)(0,255,15)
"""
