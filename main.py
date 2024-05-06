import flet as ft
from PIL import Image, ImageDraw, ImageFont
import io, base64, random, sys

big_image = ft.Image(src="Default_Large.jpg", width=300, height=300,
                     error_content=None)  # Used for displaying large image
small_image = ft.Image(src="Default_Small.jpg", width=300, height=300)  # used for displaying small image

# keeps track of the encryption images on the back end
back_image_large = Image
back_image_small = Image

# Keeps track of decryption image on the back end
decryption_image = ft.Image(src="Default_Large.jpg", width=300, height=300)
back_image_decryption = Image

temp_image = Image  # Used to make modified versions of images if need be

progress_label = ft.Text(value="Initializing...", size=25)  # Progress counters for loading screen
prev_value = ""


def main(page: ft.Page):
    page.title = "Blinder Steganography"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    textVariable = "Choose Images and Press Encrypt"
    text1 = ft.Text(textVariable)  # Used as a badly named label for most pages

    def change_progress_text(
            text):  # Changes loading screen text (Only if text has changed, so call as much as you want)
        global progress_label, prev_value
        if text != prev_value:
            progress_label.value = text
            page.update()
            prev_value = text

    # ALL CB's ARE CALLBACKS THAT HANDLE A GUI BUTON PRESS AND START THE RELATED FUNCTIONS
    def encrypt_cb_text(event):  # Button callback for encrypt button on text encryption page
        global back_image_large, back_image_small
        page.clean()
        try:
            page.clean()
            load_loading_page()
            start_loading_bar("text")
        except AttributeError:
            page.banner.content.value = "Please Select images."
            show_banner()
        except:
            # print(e)
            print(sys.exc_info())
            page.banner.content.value = "An Error Has Occurred\nPlease close the program and try again."
            show_banner()

    def test_cb(event):  # button callback for button on TESTING page
        global back_image_decryption, temp_image
        page.clean()
        change_progress_text("Start Pattern Reveal")
        load_loading_page()
        decoded = image_from_binary(back_image_decryption)

        page.clean()
        # Allows images to be viewed on FLET
        image_bytes = io.BytesIO()  # Make io byte string
        decoded.save(image_bytes, format='PNG')  # make byte stream from image
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
        new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
        page.add(new_widget)
        temp_image = decoded
        page.update()

        page.add(
            ft.Row([
                ft.ElevatedButton(
                    "Save file",
                    icon=ft.icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(
                        allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
                ),
                ft.ElevatedButton(
                    "Open Image in New Window",
                    on_click=lambda _: decoded.show()
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(), ft.Row()
        )
        load_dock()

    def encrypt_cb(event):  # Button on encrypting page
        global back_image_large, back_image_small
        try:
            if size_switch.value:
                if not does_image_fit(back_image_large, back_image_small):
                    page.clean()
                    load_loading_page()
                    change_progress_text("Calculating Image Size")

                    num = calc_max_size(back_image_large, back_image_small)
                    x1 = back_image_small.size[0] * num
                    y1 = back_image_small.size[1] * num
                    x2 = (back_image_small.size[0] * num) + 95
                    y2 = (back_image_small.size[1] * num) + 95

                    print("image 2 size:\t\t", +len(translate_image_to_binary(back_image_small)))
                    im2 = resize_image(back_image_small, x2, y2)
                    print("new image 2 size:\t", +len(translate_image_to_binary(im2)))
                    print("image 1 size:\t\t", +(back_image_large.size[0] * back_image_large.size[1] * 3))

                    print("\n")
                    print("factor:\t" + str(num))
                    print("")
                    back_image_small = im2

                    start_loading_bar()
            elif not does_image_fit(back_image_large, back_image_small):
                page.banner.content.value = "Please Select New Images or enable Image Fitting\nYour Small Image cannot fit in the Large Image without enabling Image Fitting."
                show_banner()
            elif does_image_fit(back_image_large, back_image_small) == "":
                page.banner.content.value = "Please Select New Images, Use Greyscale Encryption, or \nYour Small Image cannot fit in the Large Image without Greyscale Encryption or enabling Image Fitting."
                show_banner()
            else:  # TODO make this async or threaded or something I dont know man
                page.clean()
                load_loading_page()
                start_loading_bar()
                # x="test"
                # x = filedialog.asksaveasfile(mode="w", filetypes=[("jpg", ".jpg"), ("jpeg", ".jpeg"), ("PNG", ".png")],
                #                              defaultextension=".jpg")
                # try:
                #     encoded.save(x.name)  # , "."+x.name.split(".")[1])
                # except:
                #     encoded.convert('RGB').save(x.name)
        except AttributeError:
            page.banner.content.value = "Please Select images."
            show_banner()
        except:
            # print(e)
            print(sys.exc_info())
            page.banner.content.value = "An Error Has Occurred\nPlease close the program and try again."
            show_banner()

    def decrypt_cb(e):  # Button on Decryption page
        global back_image_decryption, temp_image
        page.clean()
        change_progress_text("Start Decryption")
        load_loading_page()
        decoded = reconstruct_image(decrypt_binary_from_image(back_image_decryption))

        page.clean()
        # Allows images to be viewed on FLET
        image_bytes = io.BytesIO()  # Make io byte string
        decoded.save(image_bytes, format='PNG')  # make byte stream from image
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
        new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
        page.add(new_widget)
        temp_image = decoded
        page.update()

        page.add(
            ft.Row([
                ft.ElevatedButton(
                    "Save file",
                    icon=ft.icons.SAVE,
                    on_click=lambda _: save_file_dialog.save_file(
                        allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
                ),
                ft.ElevatedButton(
                    "Open Image in New Window",
                    on_click=lambda _: decoded.show()
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(), ft.Row()
        )
        load_dock()

    # These callbacks are from the file pickers and save the images they pick (in memory, not on disk) to be used later
    def picker_cb_large(e: ft.FilePickerResultEvent):  # large image picker
        global big_image, back_image_large
        new_image_path = str(e.files[0].path)
        big_image.src = new_image_path
        back_image_large = Image.open(new_image_path)
        page.update()

    def picker_cb_small(e: ft.FilePickerResultEvent):  # small image picker
        global small_image, back_image_small
        new_image_path = str(e.files[0].path)
        small_image.src = new_image_path
        back_image_small = Image.open(new_image_path)
        page.update()

    def picker_cb_decrypter(e: ft.FilePickerResultEvent):  # decryption image file picker
        global decryption_image, back_image_decryption
        new_image_path = str(e.files[0].path)
        decryption_image.src = new_image_path
        back_image_decryption = Image.open(new_image_path)
        page.update()

    def save_file_result(e: ft.FilePickerResultEvent):  # same thing as the pickers but chooses the save location
        global temp_image
        valid_extensions = ['png', 'jpg', 'jpeg']
        path = e.path if e.path else False
        for i in valid_extensions:
            if i in path:
                try:
                    temp_image.save(path)

                except:
                    temp_image.convert('RGB').save(path)
                return
        path += ".png"
        try:
            temp_image.save(path)

        except:
            temp_image.convert('RGB').save(path)

    def checkbox_cb(e):  # Callback from the checkboxes to change the color of the displayed image
        global back_image_small
        if e.control.value == "grey":
            image_bytes = io.BytesIO()
            temp_image = back_image_small.copy()
            translate_image_to_greyscale(temp_image).save(image_bytes, format='PNG')

        elif e.control.value == "binary":
            image_bytes = io.BytesIO()
            temp_image = back_image_small.copy()
            translate_image_to_binaryImage(temp_image).save(image_bytes, format='PNG')

        else:
            image_bytes = io.BytesIO()
            back_image_small.save(image_bytes, format='PNG')

        image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
        small_image.src_base64 = image_base64
        page.update()

    radio_group1 = ft.RadioGroup(content=ft.Row([
        ft.Radio(label="Color", value="color"),
        ft.Radio(label="Greyscale", value="grey"),
        ft.Radio(label="Binary", value="binary")]), on_change=checkbox_cb)

    def close_banner(e):  # closes banner popup
        page.banner.open = False
        page.update()

    def show_banner():  # Opens popup banner
        page.banner.open = True
        page.update()

    def load_start_page():  # Loads the starting page (Literally just the dock and buttons for other page)
        page.clean()
        page.add(ft.Row([
            ft.Text(
                "Choose page below. \nThis program is still in beta, so expect glitches.\nIf any glitches appear, simply close and reopen the program",
                size=23)
        ], alignment=ft.MainAxisAlignment.CENTER))
        load_dock()

    def load_testing_page(e):  # Loads the testing page to view the purple and black binary image thingy
        page.clean()
        page.add(
            ft.Row([
                ft.Text("Select an image to Reveal Pixel Value Patterns")
            ], alignment=ft.MainAxisAlignment.CENTER, ),
            ft.Row([
                ft.Column([
                    decryption_image
                ], alignment=ft.MainAxisAlignment.CENTER, ),

            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton("Choose Image",
                                  on_click=lambda _: file_picker_decrypter.pick_files(
                                      allowed_extensions=["jpg", "jpeg", "png"], allow_multiple=False))
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                ft.ElevatedButton("Reveal Patterns", on_click=test_cb)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                decode_switch
            ], alignment=ft.MainAxisAlignment.CENTER)

        )
        load_dock()

    text_field = ft.TextField(label="Text", hint_text="Please enter text to encrypt")  # Text entry for text encryption

    def load_text_encryption_page(e):  # loads text encryption page. Pretty obvious I guess
        global big_image, small_image
        page.clean()
        text1.value = "Choose Image, write text, and Press Encrypt"
        page.add(
            ft.Row([
                text1
            ], alignment=ft.MainAxisAlignment.CENTER, ),
            ft.Row([
                ft.Column([
                    big_image,
                    ft.ElevatedButton("Choose Large Image",
                                      on_click=lambda _: file_picker_large.pick_files(
                                          allowed_extensions=["jpg", "jpeg", "png"], allow_multiple=False))
                ], alignment=ft.MainAxisAlignment.CENTER, ),

                ft.Column([
                    text_field
                ], alignment=ft.MainAxisAlignment.CENTER, )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(), ft.Row(),
            ft.Row([
                ft.ElevatedButton("Encrypt images", on_click=encrypt_cb_text)
            ], alignment=ft.MainAxisAlignment.CENTER)

        )
        load_dock()

    def load_encryption_page(e):  # Loads the encryption page
        global big_image, small_image
        page.clean()
        text1.value = textVariable
        page.add(
            ft.Row([
                text1
            ], alignment=ft.MainAxisAlignment.CENTER, ),
            ft.Row([
                ft.Column([
                    big_image,
                    ft.ElevatedButton("Choose Large Image",
                                      on_click=lambda _: file_picker_large.pick_files(
                                          allowed_extensions=["jpg", "jpeg", "png"], allow_multiple=False))
                ], alignment=ft.MainAxisAlignment.CENTER, ),

                ft.Column([
                    small_image,
                    ft.ElevatedButton("Choose Small Image",
                                      on_click=lambda _: file_picker_small.pick_files(
                                          allowed_extensions=["jpg", "jpeg", "png"], allow_multiple=False))
                ], alignment=ft.MainAxisAlignment.CENTER, )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                radio_group1
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                size_switch
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(), ft.Row(),
            ft.Row([
                ft.ElevatedButton("Encrypt images", on_click=encrypt_cb)
            ], alignment=ft.MainAxisAlignment.CENTER)

        )
        load_dock()

    def load_dock():  # loads the dock at the bottom of the screen to choose other pages
        page.add(
            ft.Row([
                ft.ElevatedButton("Image Encryption", on_click=load_encryption_page),
                ft.ElevatedButton("Text Encryption", on_click=load_text_encryption_page),
                ft.ElevatedButton("Image Testing", on_click=load_testing_page),
                ft.ElevatedButton("Decryption", on_click=load_decryption_page)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def load_decryption_page(e):  # loads decryption pages
        page.clean()
        page.add(
            ft.Row([
                ft.Text("Select an image to Decrypt")
            ], alignment=ft.MainAxisAlignment.CENTER, ),
            ft.Row([
                ft.Column([
                    decryption_image
                ], alignment=ft.MainAxisAlignment.CENTER, ),

            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.ElevatedButton("Choose Image",
                                  on_click=lambda _: file_picker_decrypter.pick_files(
                                      allowed_extensions=["jpg", "jpeg", "png"], allow_multiple=False))
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                ft.ElevatedButton("Decrypt Image", on_click=decrypt_cb)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                decode_switch
            ], alignment=ft.MainAxisAlignment.CENTER)

        )
        load_dock()

    def load_loading_page():  # loads loading page with the crappy text in the middle of the screen
        global progress_label
        page.add(
            ft.Row([
                progress_label
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def start_loading_bar(
            version=None):  # starts other methods based on pages. If there is any input, it forces the binary method. This is only used by the text encryption page.
        global temp_image, progress_label, back_image_small
        if version is not None:
            change_progress_text("Generating Text from Input")
            back_image_small = write_text(text_field.value)
            change_progress_text("Generating Binary")
            binary_image = translate_image_to_binaryImage(back_image_small)
            binary = translate_binaryimage_to_binarystring(binary_image)
            change_progress_text("Encoding Binary: 0%")
            encoded = encode_binary_in_image(back_image_large, binary)

            page.clean()
            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(
                ft.Row([
                    ft.ElevatedButton(
                        "Save file",
                        icon=ft.icons.SAVE,
                        on_click=lambda _: save_file_dialog.save_file(
                            allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
                    ),
                    ft.ElevatedButton(
                        "Open Image in New Window",
                        on_click=lambda _: encoded.show()
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(), ft.Row()
            )
            load_dock()
        elif radio_group1.value == "color" or radio_group1.value is None:
            change_progress_text("Generating Binary")
            binary = translate_image_to_binary(back_image_small)
            change_progress_text("Encoding Binary: 0%")
            encoded = encode_binary_in_image(back_image_large, binary)

            page.clean()

            # Allows images to be viewed on FLET
            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(
                ft.Row([
                    ft.ElevatedButton(
                        "Save file",
                        icon=ft.icons.SAVE,
                        on_click=lambda _: save_file_dialog.save_file(
                            allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
                    ),
                    ft.ElevatedButton(
                        "Open Image in New Window",
                        on_click=lambda _: encoded.show()
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(), ft.Row()
            )
            load_dock()

            # reconstruct_image(decrypt_binary_from_image(encoded)).show()
        elif radio_group1.value == "grey":
            change_progress_text("Generating Binary")
            grey = translate_image_to_greyscale(back_image_small)
            binary = translate_greyscale_to_binary(grey)
            change_progress_text("Encoding Binary: 0%")
            encoded = encode_binary_in_image(back_image_large, binary)

            page.clean()

            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(
                ft.Row([
                    ft.ElevatedButton(
                        "Save file",
                        icon=ft.icons.SAVE,
                        on_click=lambda _: save_file_dialog.save_file(
                            allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
                    ),
                    ft.ElevatedButton(
                        "Open Image in New Window",
                        on_click=lambda _: encoded.show()
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(), ft.Row()
            )
            load_dock()
        else:
            change_progress_text("Generating Binary")
            binary_image = translate_image_to_binaryImage(back_image_small)
            binary = translate_binaryimage_to_binarystring(binary_image)
            change_progress_text("Encoding Binary: 0%")
            encoded = encode_binary_in_image(back_image_large, binary)

            page.clean()
            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(
                ft.Row([
                    ft.ElevatedButton(
                        "Save file",
                        icon=ft.icons.SAVE,
                        on_click=lambda _: save_file_dialog.save_file(
                            allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
                    ),
                    ft.ElevatedButton(
                        "Open Image in New Window",
                        on_click=lambda _: encoded.show()
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(), ft.Row()
            )
            load_dock()

    """++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
    """For ease of view, everything below here is the Dense Encoding Method and functions."""
    """++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

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
        smaller_size_alt = small_width * small_height

        if small_size + 34 < big_size:
            return True
        elif small_size_alt + 34 < big_size:
            return ""
        elif smaller_size_alt + 34 < big_size:
            return "b"
        else:
            return False

    # Get encoded binary from image
    def decrypt_binary_from_image(image):
        change_progress_text("Decoding Binary From Image...")
        im_width, im_height = image.size
        binary_string = ""
        prog_counter = 0
        total_progress = image.size[0] * image.size[1]
        for i in range(im_width):
            for j in range(im_height):
                prog_counter += 1

                prog = (100 * prog_counter // total_progress)

                change_progress_text("Decoding Binary: " + str(prog) + "%")
                for color in image.getpixel((i, j)):
                    if is_even(color):
                        binary_string += str(0)
                    else:
                        binary_string += str(1)
        if decode_switch.value:
            return full_service_decryption(binary_string)
        else:
            return binary_string

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

    # makes an image a binary image (either black or white for each pixel
    def translate_image_to_binaryImage(image):
        # Convert the image to grayscale
        gray_image = image.convert('L')

        # Apply thresholding to convert to binary image
        binary_threshold = 127
        binary_image = gray_image.point(lambda x: 255 if x > binary_threshold else 0, '1')

        # Display or save the binary image
        return binary_image

    # Translates a binary image to a binary string
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

    # Normally, binary string extends only part of the image, this extends it to cover the whol thing
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

                prog = (100 * prog_counter // total_progress)

                change_progress_text("Encoding Binary: " + str(prog) + "%")

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
                change_progress_text("Generating Image: " + str(100 * prog_counter // total_progress) + "%")

        return new_image

    # Rebuilds a color image from the binary string
    def reconstruct_image(binary_string):
        change_progress_text("Reconstructing Image...")
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

    # Reconstructs an image if its in full color
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

    # Reconstructs an image if its in greyscale
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

    # Reconstructs an image if its a binary image
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

    # Resizes an image to fit a new size (must be integers)
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

    # Calculates the max size for one image fitting into another
    def calc_max_size(big_image, small_image, method=None):
        big_width, big_height = big_image.size
        small_width, small_height = small_image.size
        big_size = big_width * big_height * 3

        if method == "g":
            small_size = (small_width * small_height * 8) + 34
        elif method == "b":
            small_size = (small_width * small_height) + 34
        elif method is None:
            small_size = (small_width * small_height * 24) + 34

        if big_size >= small_size:
            return None
        else:
            return big_size / small_size

    # Puts text into a picture for encrypting.
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

    # Encrypts using the weird method I found online, takes a key and text that must be the same length
    def one_time_pad_encrypt(plaintext, key):
        if len(plaintext) != len(key):
            raise ValueError("Message and key must be of the same length")
        encrypted_message = ''
        for i in range(len(plaintext)):
            encrypted_message += str(int(plaintext[i]) ^ int(key[i]))
        return encrypted_message

    # Its circular so decrypting is the same as encrypting
    def one_time_pad_decrypt(ciphertext, key):
        return one_time_pad_encrypt(ciphertext, key)

    # Fully encrypts a string in chunks of 8
    def full_service_encryption(binary_string):
        # Encrypt
        change_progress_text("Encrypting Binary String")
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

    # Fully decrypts a string in chunks of 8
    def full_service_decryption(binary_string):
        # Decrypt
        change_progress_text("Decrypting Binary String")
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

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    """INITIALIZE VALUES HERE"""

    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Please Select New Images\nEither your Small Image cannot fit in the Large Image, or you have not chosen images."
            , color=ft.colors.BLACK),
        actions=[
            ft.IconButton(ft.icons.CANCEL, icon_color=ft.colors.BLUE, on_click=close_banner),
        ],
    )

    # image_path = "Golden.jpg"
    # image_widget = ft.Image(src=image_path, width=100, height=100)

    file_picker_large = ft.FilePicker(on_result=picker_cb_large)
    page.overlay.append(file_picker_large)

    file_picker_small = ft.FilePicker(on_result=picker_cb_small)
    page.overlay.append(file_picker_small)

    file_picker_decrypter = ft.FilePicker(on_result=picker_cb_decrypter)
    page.overlay.append(file_picker_decrypter)

    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(save_file_dialog)

    size_switch = ft.Switch(label="Enabling Image Fitting", value=False)
    decode_switch = ft.Switch(label="Enable Decoding Binary? (disabling will lead to garbled images)",
                              label_position=ft.LabelPosition.LEFT, value=True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    load_start_page()  # Load first page on page creation


ft.app(target=main, assets_dir="assets")  # USE THIS FOR APP
# ft.app(target=main, port=8000, view=ft.AppView.WEB_BROWSER) #USE THIS FOR WEB BROWSER
