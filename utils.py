from config import *
from PIL import Image


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

    # get all colours in image and sort in descending order of pixel count
    colours = img.getcolors(maxcolors=num_pixels)
    colours.sort(reverse=True)

    # keep only the top most frequent colours
    frequent_colours = colours[:NUMBER_OF_COLOURS]

    # create colour palette
    colour_palette = []
    for colour in frequent_colours:
        r, g, b, *a = colour[1]
        hex = f"#{r:02x}{g:02x}{b:02x}"
        percentage = f"{colour[0] / num_pixels:.2%}"

        colour_palette.append(
            {
                "count": colour[0],
                "rgb": colour[1],
                "hex": hex,
                "percentage": percentage,
            }
        )

    return frequent_colours
