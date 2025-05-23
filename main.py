"""
A website that creates a colour palette based on the 10 most common colours in an uploaded image.
"""

from os import urandom
from file_upload_form import FileUploadForm
from utils import is_allowed_file, process_file
from flask import Flask, render_template, request


app = Flask(__name__)

# secret key generation for form usage
app.config["SECRET_KEY"] = urandom(32)


@app.route("/", methods=["GET", "POST"])
def home():
    image = None
    colours = None
    form = FileUploadForm()

    if form.validate_on_submit():
        img_file = request.files["file"]

        if is_allowed_file(img_file.filename):
            image, colours = process_file(img_file)

    return render_template("index.html", form=form, image=image, colours=colours)


if __name__ == "__main__":
    app.run(debug=True)
