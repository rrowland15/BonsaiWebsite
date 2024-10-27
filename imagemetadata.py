from exif import Image

with open('static/images/goldjun.jpg', 'rb') as image_file:
    image = Image(image_file)

if image.has_exif:
    print("Image has EXIF data.")
    print(image.get("datetime")) # Access specific metadata like datetime
    print(image.get("model")) # Access camera model
    # Access more metadata as needed
else:
    print("Image does not have EXIF data.")