from PIL import Image, ImageDraw, ImageFont
import random

"""This is the file that is attempting to encode 1s and 0s in the R B and G values separately"""

def is_even(num):  # Checks if a number is even
    if num % 2 == 0:
        return True
    else:
        return False


# Checks to see if one image will fit inside another image
def does_image_fit(big_image, small_image):
    big_width, big_height = big_image.size
    small_width, small_height = small_image.size

    big_size = big_width * big_height * 3

    small_size = small_width * small_height * 24
    small_size_alt = small_width * small_height * 8

    if small_size + 33 < big_size:
        return True
    elif small_size_alt + 33 < big_size:
        return ""
    else:
        return False


# Get encoded binary from image
def decrypt_binary_from_image(image):
    im_width, im_height = image.size
    binary_string = ""
    for i in range(im_width):
        for j in range(im_height):
            for color in image.getpixel((i, j)):
                if is_even(color):
                    binary_string += str(0)
                else:
                    binary_string += str(1)
    return full_service_decryption(binary_string)


# Changes an image from color to greyscale
def translate_image_to_greyscale(image):
    image2 = image.copy()
    image2 = image2.convert("L")
    # image_width, image_height = image2.size
    # pixels = image2.load()
    # for i in range(image_width):
    #     for j in range(image_height):
    #         try:
    #             r, g, b = image2.getpixel((i, j))
    #         except:
    #             r, g, b, a = image2.getpixel((i, j))
    #         avg = (r + g + b) // 3
    #         pixels[i, j] = (avg, avg, avg)
    return image2


def translate_image_to_binaryImage(image):
    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Apply thresholding to convert to binary image
    binary_threshold = 127
    binary_image = gray_image.point(lambda x: 255 if x > binary_threshold else 0, '1')

    # Display or save the binary image
    return binary_image


def translate_binaryimage_to_binarystring(image):
    binary_string = ''
    image_width, image_height = image.size
    for i in range(image_width):
        for j in range(image_height):
            r = image.getpixel((i, j))
            if r == 0:
                binary_string += "1"
            else:
                binary_string += "0"
    binary_width = "{:0{}b}".format(image_width, 16)
    binary_height = "{:0{}b}".format(image_height, 16)
    binary_string = binary_width + binary_height + "10" + binary_string
    return binary_string


# Translates a greyscale image to binary
def translate_greyscale_to_binary(image):
    binary_string = ''
    image_width, image_height = image.size
    for i in range(image_width):
        for j in range(image_height):
            r = image.getpixel((i, j))
            # Convert each RGB value to binary and concatenate them
            binary_string += '{:08b}'.format(r)
    binary_width = "{:0{}b}".format(image_width, 16)
    binary_height = "{:0{}b}".format(image_height, 16)
    binary_string = binary_width + binary_height + "01" + binary_string
    return binary_string


# Translates an image to binary
def translate_image_to_binary(image):  # makes binary string from image
    binary_string = ''
    image_width, image_height = image.size
    for i in range(image_width):
        for j in range(image_height):
            r, g, b = image.getpixel((i, j))
            # Convert each RGB value to binary and concatenate them
            binary_string += '{:08b}{:08b}{:08b}'.format(r, g, b)
    binary_width = "{:0{}b}".format(image_width, 16)
    binary_height = "{:0{}b}".format(image_height, 16)
    binary_string = binary_width + binary_height + "00" + binary_string
    return binary_string


def extend_binary_to_whole_image(image_width, image_height, binary_string):
    total_pixels = image_width * image_height
    if len(binary_string) + 8 < total_pixels:
        diff = ((total_pixels * 3) - len(binary_string)) // 8
        binary_choices = []
        for i in range(len(binary_string)):
            binary_choices.append(int(binary_string[i:i + 8], 2))
            i += 8  # Move index to the next pixel
        for i in range(diff):
            number = random.choice(binary_choices)
            binary_string += str("{:08b}".format(number))
    return binary_string


# Encodes a binary string inside an image using the dense encoding method
def encode_binary_in_image(image, binary_string):  # adds binary to image

    prog_counter = 0
    total_progress = image.size[0] * image.size[1]

    im_width, im_height = image.size
    counter = 0

    pixels = image.load()

    binary_string = extend_binary_to_whole_image(im_width, im_height, binary_string)

    binary_string = full_service_encryption(binary_string)

    for i in range(im_width):
        for j in range(im_height):

            prog_counter += 1
            print(100 * prog_counter // total_progress)

            if counter < len(binary_string):
                r, g, b = pixels[i, j]
                if counter < len(binary_string):
                    if binary_string[counter] == '1' and r % 2 == 0:
                        r += 1
                    elif binary_string[counter] == '0' and r % 2 == 1:
                        r -= 1
                counter += 1

                if counter < len(binary_string):
                    if binary_string[counter] == '1' and g % 2 == 0:
                        g += 1
                    elif binary_string[counter] == '0' and g % 2 == 1:
                        g -= 1
                counter += 1

                if counter < len(binary_string):
                    if binary_string[counter] == '1' and b % 2 == 0:
                        b += 1
                    elif binary_string[counter] == '0' and b % 2 == 1:
                        b -= 1
                counter += 1

            else:
                r, g, b = pixels[i, j]
                r += random.randint(-1, 1)
                g += random.randint(-1, 1)
                b += random.randint(-1, 1)
                counter += 1

            pixels[i, j] = (r, g, b)
    return image


# Reveals the encoded data in the image
def image_from_binary(image):
    prog_counter = 0
    total_progress = image.size[0] * image.size[1]
    new_image = image
    im_width, im_height = image.size
    for i in range(im_width):
        for j in range(im_height):
            try:
                R, G, B = new_image.getpixel((i, j))
            except:
                R, G, B, A = new_image.getpixel((i, j))
            if R % 2 == 0 and G % 2 == 0 and B % 2 == 0:
                new_image.putpixel((i, j), (0, 0, 0))
            elif R % 2 == 1 and G % 2 == 1 and B % 2 == 1:
                new_image.putpixel((i, j), (255, 255, 255))
            else:
                new_image.putpixel((i, j), (255, 0, 210))
                # print("ERROR: " + str(i) + " " + str(j))
            prog_counter += 1
            print(100 * prog_counter // total_progress)

    return new_image


# Rebuilds a color image from the binary string
def reconstruct_image(binary_string):
    im_width, im_height = (int(binary_string[0:16], 2), int(binary_string[16:32], 2))  # get encoded size
    # print(im_width, im_height)
    # print(binary_string[32:34])
    if int(binary_string[32:34]) == 0:
        print("Color")
        return color_reconstruction(binary_string, im_width, im_height)
    elif int(binary_string[32:34]) == 1:
        print("Grey")
        return grey_reconstruction(binary_string, im_width, im_height)
    else:
        print("binary")
        return binary_reconstruction(binary_string, im_width, im_height)


def color_reconstruction(binary_string, im_width, im_height):
    image = Image.new("RGB", (im_width, im_height))

    total_size = im_width * im_height

    # Load pixel data
    pixels = image.load()

    # Iterate through the binary string and set pixel values
    index = 34  # start at 34 so that you dont include the 2 sets of 16 bits thing at the start for size, and 2 bits for grey or binary

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


def grey_reconstruction(binary_string, im_width, im_height):
    image = Image.new("RGB", (im_width, im_height))

    # Load pixel data
    pixels = image.load()

    # Iterate through the binary string and set pixel values
    index = 34  # start at 34 so that you dont include the 2 sets of 16 bits thing at the start for size, and 2 bits for grey or binary

    for i in range(im_width):
        for j in range(im_height):
            if index + 8 < len(binary_string):
                # Extract RGB values from the binary string
                r = int(binary_string[index:index + 8], 2)
                g = r
                b = r
                index += 8  # Move index to the next pixel

                # Set pixel value in the reconstructed image
                pixels[i, j] = (r, g, b)

    # Save the reconstructed image to a file
    return image


def binary_reconstruction(binary_string, im_width, im_height):
    image = Image.new("RGB", (im_width, im_height))
    # Load pixel data
    pixels = image.load()

    # Iterate through the binary string and set pixel values
    index = 34  # start at 34 so that you dont include the 2 sets of 16 bits thing at the start for size, and 2 bits for grey or binary

    for i in range(im_width):
        for j in range(im_height):
            if index + 8 < len(binary_string):
                if binary_string[index] == "1":
                    pixels[i, j] = (0, 0, 0)
                else:
                    pixels[i, j] = (255, 255, 2552)
                index += 1
    return image


def resize_image(img, new_width, new_height):
    new_width = int(new_width)
    new_height = int(new_height)
    oldWidth, oldHeight = img.size
    newPhotoImage = Image.new("RGB", (new_width, new_height))
    pixels1 = img.load()
    pixels2 = newPhotoImage.load()
    for x in range(new_width):
        for y in range(new_height):
            xOld = int(x * oldWidth / new_width)
            yOld = int(y * oldHeight / new_height)
            pixels2[x, y] = pixels1[xOld, yOld]
    return newPhotoImage


def calc_max_size(big_image, small_image, method=None):
    big_width, big_height = big_image.size
    small_width, small_height = small_image.size
    big_size = big_width * big_height * 3

    if method == "g":
        small_size = (small_width * small_height * 8) + 33
    elif method == "b":
        # TODO
        raise RuntimeError("BINARY CALCULATION (OR BINARY ENCODING) IS NOT IMPLEMENTED YET")
    elif method is None:
        small_size = (small_width * small_height * 24) + 33

    if big_size >= small_size:
        return None
    else:
        return big_size / small_size


def write_text(input_text):
    text = input_text.upper()
    for i in range(len(text)):
        if text[i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ,.?!' ":
            text = text.replace(text[i], '@')

    image = Image.new("RGB", (len(text) * 5, 5))
    # Create a drawing context
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("assets/pixel.ttf", size=5)  # Use your desired font and size
    color = (255, 255, 255)  # White color, you can change it as needed
    position = (0, 0)  # Text position (x, y)

    # Draw the text on the image
    draw.text(position, text, fill=color, font=font)

    # Save or display the modified image
    return image  # Return final image


def one_time_pad_encrypt(plaintext, key):
    if len(plaintext) != len(key):
        raise ValueError("Message and key must be of the same length")
    encrypted_message = ''
    for i in range(len(plaintext)):
        encrypted_message += str(int(plaintext[i]) ^ int(key[i]))
    return encrypted_message
    # if len(plaintext) != len(key):
    #     raise ValueError("Plaintext and key must be of the same length")
    # return ''.join(str(int(a) ^ int(b)) for a, b in zip(plaintext, key))


def one_time_pad_decrypt(ciphertext, key):
    return one_time_pad_encrypt(ciphertext, key)

def full_service_encryption(binary_string):
    # Encrypt
    temp_index = 8
    new_binary = list(binary_string)
    original_bits = binary_string[:8]  # Store the original 8 bits
    for i in range((len(binary_string) // 8) - 1):  # Adjusted loop boundary
        # Extract the key from the previous plaintext block
        key = new_binary[temp_index - 8:temp_index]
        new_binary[temp_index:temp_index + 8] = one_time_pad_encrypt(binary_string[temp_index:temp_index + 8], key)
        temp_index += 8
    new_binary = ''.join(new_binary)
    return new_binary

def full_service_decryption(binary_string):
    # Decrypt
    temp_index = 8  # Start at 8 to skip the first 8 bits
    new_binary = list(binary_string)
    previous_bits = binary_string[:8]
    for i in range((len(binary_string) // 8) - 1):  # Adjusted loop boundary
        # Extract the key from the previous ciphertext block
        key = binary_string[temp_index - 8:temp_index]
        new_binary[temp_index:temp_index + 8] = one_time_pad_decrypt(binary_string[temp_index:temp_index + 8], key)
        temp_index += 8

    new_binary = "".join(new_binary)
    return new_binary


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# encoded = Image.open("testing/EncodedV3.1.png")
# reconstruct_image(decrypt_binary_from_image(encoded)).show()
#
# sys.exit()
#
# im1 = Image.open("testing/test.jpg")
# im2 = Image.open('testing/Golden.jpg')
# num = calc_max_size(im1, im2)
# im2 = resize_image(im2,im1.size[0] * num,im1.size[1] * num)


# # # im2 = Image.open("testing/Gruddling.jpg")
# #
# if not does_image_fit(im1, im2):
#     print("Picture does not fit")
#
# else:
#     pass
#     #     binary_image = translate_image_to_binaryImage(im2)
#     #     binary_image.show()
#     #     b_string = translate_binaryimage_to_binarystring(binary_image)
#     greyscale = translate_image_to_greyscale(im2)
#     # greyscale.show()
#     # im2.show()
#     b_string = translate_greyscale_to_binary(greyscale)
#
#     encoded = encode_binary_in_image(im1, b_string)
#     # encoded.show()
#     # image_from_binary(encoded.copy()).show()  # include copy so it doesn't fuck up the original
#     reconstruct_image(decrypt_binary_from_image(encoded)).show()
#
# # im1.show()
#
#     binary = translate_image_to_binary(im2)
#     #
#     encoded = encode_binary_in_image(im1, binary)
#     #
#     encoded.show()
#
#     x = filedialog.asksaveasfile(mode="w", filetypes=[("jpg", ".jpg"), ("jpeg", ".jpeg"), ("PNG", ".png")],
#                                  defaultextension=".jpg")
#     try:
#         encoded.save(x.name)  # , "."+x.name.split(".")[1])
#     except:
#         encoded.convert('RGB').save(x.name)
#     #
#     # # image_from_binary(encoded.copy()).show()  # include copy so it doesn't fuck up the original
#     #
#     # # print(decrypt_binary_from_image(encoded))
#     # reconstruct_image(decrypt_binary_from_image(encoded)).show()
