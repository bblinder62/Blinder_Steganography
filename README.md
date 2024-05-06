# Blinder_Steganography
Project for Brandeis CS107: Introduction to Computer Security. 

This project implements a modified custom Steganography method 
with a GUI. I created this because every steganography tool online
can be decrypted by every other steganography tool online.
This project was created with the expressed intention of
making a steganography method that cannot be automatically
decrypted by tools online.

The custom method I created was to take the smaller image,
convert it into a binary string pixel by pixel, encode that with
a custom cipher that encodes 8 bits at a time using the previous 8 bits
as the key for the next 8 bits. Then it encodes that binary
into the target image pixel by pixel using the 3 color 
channels of the target image. Each channel is made odd for a 1
and even for a 0, so the entire image can be easily encoded.

The program can also encrypt greyscale or binary images to save
some space.

The program can obviously encrypt and decrypt, but it can also
print out a modified version of the picture that shows patterns
in the pixels of the image. It is a holdover from when I used a
less efficient version of encoding, but still reveals many 
patterns. Pink means a mix of even and odd, black is all odd,
and white is all even. 

## Running
The GUI is made using Flet, a python GUI library. It also
allows for automatic exporting of the files as executable applications.
Details can be found here https://flet.dev/docs/cookbook/packaging-desktop-app/.
