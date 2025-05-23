from PIL import Image
from config import *


def allowed_file(filename: str) -> bool:
    """
    Return True if the filename is allowed. False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def most_frequent_colours(
    img: Image.Image,
) -> list[tuple[int, tuple[int, int, int], str]]:
    """
    Return a list of the most common colours in an image.
    Each list item contains the colour frequency, RGB values, HEX value, and percentage in that order.
    """

    # number of pixels in the image
    width, height = img.size
    num_pixels = width * height

    # get all colours in image and sort in descending order of frequency
    all_colours = img.getcolors(maxcolors=num_pixels)
    all_colours.sort(reverse=True)

    # keep only the most frequent colours
    frequent_colours = all_colours[:NUMBER_OF_COLOURS]

    # add hex code and percentage to frequent colours list
    for i in range(len(frequent_colours)):
        r, g, b, *a = frequent_colours[i][1]
        hex = f"#{r:02x}{g:02x}{b:02x}"
        percentage = f"{frequent_colours[i][0] / num_pixels:.2%}"
        frequent_colours[i] = frequent_colours[i] + (hex, percentage)

    return frequent_colours
