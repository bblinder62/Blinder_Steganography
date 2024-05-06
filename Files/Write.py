import string

from PIL import Image, ImageDraw, ImageFont

# Open the image


# # Specify text properties
# text = "How long can this go I dont know pretty long its neat here's some weird characters $(*)!@*# and here's a few normal ones. I am sam, but why? WHY!"
# # text=input("Text for file:\t")
# text = text.upper()
#
# for i in range(len(text)):
#     if text[i] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ,.?!' ":
#         text = text.replace(text[i], '@')
#
# image = Image.new("RGB", (len(text) * 5, 5))
# ''
# # Create a drawing context
# draw = ImageDraw.Draw(image)
#
# font = ImageFont.truetype("assets/pixel.ttf", size=5)  # Use your desired font and size
# color = (255, 255, 255)  # White color, you can change it as needed
# position = (0, 0)  # Text position (x, y)
#
# # Draw the text on the image
# draw.text(position, text, fill=color, font=font)
#
# # Save or display the modified image
# image.show()  # Display the modified image


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

write_text("How long can this go I dont know pretty long its neat here's some weird characters $(*)!@*# and here's a few normal ones. I am sam, but why? WHY!").show()
