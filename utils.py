from config import *
from PIL import Image
from io import BytesIO
from base64 import b64encode


def is_allowed_file(filename: str) -> bool:
    """
    Return True if the filename is allowed. False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def frequent_colours_palette(
    img: Image.Image,
) -> list[dict[tuple[int, int, int], str, str]]:
    """
    Return a colour palette of the most frequent colours in an image.
    Each dictionary item contains the pixel count, RGB values, HEX value, and percentage.
    """

    # number of pixels in the image
    width, height = img.size
    num_pixels = width * height

    # get all colours in image and sort in descending order of pixel count
    colours = img.getcolors(maxcolors=num_pixels)
    colours.sort(reverse=True)

    # keep only the most frequent colours
    frequent_colours = colours[:NUMBER_OF_COLOURS]

    # create colour palette
    colour_palette = []
    for colour in frequent_colours:
        count, rgb = colour
        percentage = f"{count / num_pixels:.2%}"
        r, g, b, *a = rgb
        hex = f"#{r:02x}{g:02x}{b:02x}"

        colour_palette.append(
            {
                "rgb": rgb,
                "hex": hex,
                "percentage": percentage,
            }
        )

    return colour_palette


def process_file(file):
    """
    Process an image file returning its colour palette and base64 image string.
    """

    # load image into memory and convert to file-like memory object
    img_data = BytesIO(file.read())

    # create Image object
    img = Image.open(img_data)

    # get most frequent colours of the image
    colours = frequent_colours_palette(img)

    # convert image to base64 string and utf-8 decode for display in browser
    img_base64 = b64encode(img_data.getvalue()).decode("utf-8")

    return img_base64, colours
