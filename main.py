"""
A website that creates a colour palette based on the 10 most common colours in an uploaded image.
"""

from os import urandom
from flask import Flask, render_template, request
from file_upload_form import FileUploadForm
from io import BytesIO
from base64 import b64encode
from PIL import Image

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "jfif"}

app = Flask(__name__)

# secret key generation for form usage
app.config["SECRET_KEY"] = urandom(32)


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


@app.route("/", methods=["GET", "POST"])
def home():
    form = FileUploadForm()
    image = None
    colours = None

    if form.validate_on_submit():
        file = request.files["file"]

        if allowed_file(file.filename):
            # load image into memory and convert to file-like memory object
            img_data = BytesIO(file.read())

            # create Image object
            img = Image.open(img_data)

            # get most frequent colours of the image
            frequent_colours = most_frequent_colours(img)

            # convert image to base64 string and utf-8 decode for display in browser
            img_base64 = b64encode(img_data.getvalue()).decode("utf-8")

            return render_template(
                "index.html", form=form, image=img_base64, colours=frequent_colours
            )

    return render_template("index.html", form=form, image=image, colours=colours)


if __name__ == "__main__":
    app.run(debug=True)