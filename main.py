"""
A website that creates a colour palette based on the 10 most common colours in an uploaded image.
"""

from os import urandom
from flask import Flask, render_template, request
from file_upload_form import FileUploadForm
from io import BytesIO
from base64 import b64encode
from utils import allowed_file, most_frequent_colours
from PIL import Image


app = Flask(__name__)

# secret key generation for form usage
app.config["SECRET_KEY"] = urandom(32)


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
