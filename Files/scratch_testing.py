from PIL import Image
from Files import DenseEncoding as de

im1 = Image.open('../testing/test.jpg')
# im2 = Image.open('/Users/benblinder/Documents/GitHub/CS107/Project/testing/TestEncoded.jpg')
im2 = Image.open('../testing/Gruddling.jpg')
im2.show()
if not de.does_image_fit(im1, im2):
    num = de.calc_max_size(im1, im2)
    x1=im2.size[0] * num
    y1=im2.size[1] * num
    x2=(im2.size[0] * num) + 95
    y2=(im2.size[1] * num) + 95

    print("image 2 size:\t\t", +len(de.translate_image_to_binary(im2)))
    im2 = de.resize_image(im2, x2, y2)
    print("new image 2 size:\t", +len(de.translate_image_to_binary(im2)))
    print("image 1 size:\t\t", +(im1.size[0]*im1.size[1] * 3))

    print("\n")
    print("factor:\t"+str(num))
    print("")
    im2.show()


else:
    pass

# binary = de.translate_image_to_binary(im2)
#
# encoded = de.encode_binary_in_image(im1, binary)
#
# encoded.show()
#
# de.image_from_binary(encoded.copy()).show()  # include copy so it doesn't fuck up the original
#
# de.reconstruct_image(de.decrypt_binary_from_image(encoded)).show()

# print(x1, y1)
# print(x2, y2)
