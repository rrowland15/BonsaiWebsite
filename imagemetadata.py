
def get_image_info(file):
    from exif import Image

    image = Image(file)

    if image.has_exif:
        print("Image has EXIF data.")
        print(image.get("datetime")) # Access specific metadata like datetime
        print(image.get("model")) # Access camera model
        # Access more metadata as needed
    else:
        print("Image does not have EXIF data.")