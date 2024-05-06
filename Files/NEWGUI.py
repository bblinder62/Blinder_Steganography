import sys

import flet as ft
from PIL import Image
from Files import DenseEncoding as DE
import io, base64

big_image = ft.Image(src="Default_Large.jpg", width=300, height=300, error_content=None)
small_image = ft.Image(src="Default_Small.jpg", width=300, height=300)

back_image_large = Image
back_image_small = Image

decryption_image = ft.Image(src="Default_Large.jpg", width=300, height=300)
back_image_decryption = Image

temp_image = Image


def main(page: ft.Page):
    page.title = "Blinder Steganography"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    textVariable = "Choose Images and Press Encrypt"
    text1 = ft.Text(textVariable)

    def encrypt_cb(event):
        global back_image_large, back_image_small
        try:
            if size_switch.value:
                if not DE.does_image_fit(back_image_large, back_image_small):
                    page.clean()
                    num = DE.calc_max_size(back_image_large, back_image_small)
                    x1 = back_image_small.size[0] * num
                    y1 = back_image_small.size[1] * num
                    x2 = (back_image_small.size[0] * num) + 95
                    y2 = (back_image_small.size[1] * num) + 95

                    print("image 2 size:\t\t", +len(DE.translate_image_to_binary(back_image_small)))
                    im2 = DE.resize_image(back_image_small, x2, y2)
                    print("new image 2 size:\t", +len(DE.translate_image_to_binary(im2)))
                    print("image 1 size:\t\t", +(back_image_large.size[0] * back_image_large.size[1] * 3))

                    print("\n")
                    print("factor:\t" + str(num))
                    print("")
                    back_image_small = im2


                    load_loading_page()
                    start_loading_bar()
            elif not DE.does_image_fit(back_image_large, back_image_small):
                page.banner.content.value = "Please Select New Images or enable Image Fitting\nYour Small Image cannot fit in the Large Image without enabling Image Fitting."
                show_banner()
            elif DE.does_image_fit(back_image_large, back_image_small) == "":
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

    def decrypt_cb(e):
        global back_image_decryption
        # print("Start Decryption")
        DE.reconstruct_image(DE.decrypt_binary_from_image(back_image_decryption)).show()
        # print("Finished")

    def picker_cb_large(e: ft.FilePickerResultEvent):
        global big_image, back_image_large
        new_image_path = str(e.files[0].path)
        big_image.src = new_image_path
        back_image_large = Image.open(new_image_path)
        page.update()

    def picker_cb_small(e: ft.FilePickerResultEvent):
        global small_image, back_image_small
        new_image_path = str(e.files[0].path)
        small_image.src = new_image_path
        back_image_small = Image.open(new_image_path)
        page.update()

    def picker_cb_decrypter(e: ft.FilePickerResultEvent):
        global decryption_image, back_image_decryption
        new_image_path = str(e.files[0].path)
        decryption_image.src = new_image_path
        back_image_decryption = Image.open(new_image_path)
        page.update()

    def save_file_result(e: ft.FilePickerResultEvent):
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

    def checkbox_cb(e):
        global back_image_small
        if e.control.value == "grey":
            image_bytes = io.BytesIO()
            temp_image = back_image_small.copy()
            DE.translate_image_to_greyscale(temp_image).save(image_bytes, format='PNG')

        elif e.control.value == "binary":
            image_bytes = io.BytesIO()
            temp_image = back_image_small.copy()
            DE.translate_image_to_binaryImage(temp_image).save(image_bytes, format='PNG')

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

    def close_banner(e):
        page.banner.open = False
        page.update()

    def show_banner():
        page.banner.open = True
        page.update()

    def load_start_page():
        page.clean()
        load_dock()

    def load_encryption_page(e):
        global big_image, small_image
        page.clean()
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

    def load_dock():
        page.add(
            ft.Row([
                ft.ElevatedButton("Encryption Page", on_click=load_encryption_page),
                ft.ElevatedButton("Decryption Page", on_click=load_decryption_page)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def load_decryption_page(e):
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
            ], alignment=ft.MainAxisAlignment.CENTER)

        )
        load_dock()

    def load_loading_page():
        pass

    def start_loading_bar():
        global temp_image
        if radio_group1.value == "color" or radio_group1.value is None:
            binary = DE.translate_image_to_binary(back_image_small)
            encoded = DE.encode_binary_in_image(back_image_large, binary)

            # Allows images to be viewed on FLET
            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(ft.ElevatedButton(
                "Save file",
                icon=ft.icons.SAVE,
                on_click=lambda _: save_file_dialog.save_file(
                    allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
            ))
            load_dock()

            # DE.reconstruct_image(DE.decrypt_binary_from_image(encoded)).show()
        elif radio_group1.value == "grey":
            grey = DE.translate_image_to_greyscale(back_image_small)
            binary = DE.translate_greyscale_to_binary(grey)
            encoded = DE.encode_binary_in_image(back_image_large, binary)
            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(ft.ElevatedButton(
                "Save file",
                icon=ft.icons.SAVE,
                on_click=lambda _: save_file_dialog.save_file(
                    allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
            ))
            load_dock()
        else:
            binary_image = DE.translate_image_to_binaryImage(back_image_small)
            binary = DE.translate_binaryimage_to_binarystring(binary_image)
            encoded = DE.encode_binary_in_image(back_image_large, binary)
            image_bytes = io.BytesIO()  # Make io byte string
            encoded.save(image_bytes, format='PNG')  # make byte stream from image
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')  # Make byte string base64 encoded
            new_widget = ft.Image(src_base64=image_base64, width=640, height=480)  # add image to screen
            page.add(new_widget)
            temp_image = encoded
            page.update()

            page.add(ft.ElevatedButton(
                "Save file",
                icon=ft.icons.SAVE,
                on_click=lambda _: save_file_dialog.save_file(
                    allowed_extensions=["jpg", "jpeg", "png"], file_name="image.png")
            ))
            load_dock()

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
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    load_start_page()  # Load first page on page creation


ft.app(target=main, assets_dir="../assets")  # USE THIS FOR APP
# ft.app(target=main, port=8000, view=ft.AppView.WEB_BROWSER) #USE THIS FOR WEB BROWSER
