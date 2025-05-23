from PIL import Image
from config import ALLOWED_EXTENSIONS


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def most_frequent_colours(
    img: Image.Image,
) -> list[tuple[int, tuple[int, int, int], str]]:
    # determine maximum possible colours of the image
    max_colours = img.size[0] * img.size[1]

    # get all colours in image and sort descending
    all_colours = img.getcolors(maxcolors=max_colours)
    all_colours.sort(reverse=True)

    # keep only top 10 colours
    frequent_colours = all_colours[:10]

    # add hex code and percentage to frequent colours list
    for i in range(len(frequent_colours)):
        r, g, b, *a = frequent_colours[i][1]
        hex = f"#{r:02x}{g:02x}{b:02x}"
        percentage = f"{frequent_colours[i][0] / max_colours:.2%}"
        frequent_colours[i] = frequent_colours[i] + (hex, percentage)

    return frequent_colours
