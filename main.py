"""
A website that creates a colour palette based on the most common colours in an uploaded image.
"""

from os import getenv
from dotenv import load_dotenv
from file_upload_form import FileUploadForm
from flask import Flask, render_template, request
from utils import is_allowed_file, process_image_file


app = Flask(__name__)

# set secret key
load_dotenv()
app.config["SECRET_KEY"] = getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    image = None
    colours = None
    form = FileUploadForm()

    if form.validate_on_submit():
        img_file = request.files["file"]

        if is_allowed_file(img_file.filename):
            image, colours = process_image_file(img_file)

    return render_template("index.html", form=form, image=image, colours=colours)


if __name__ == "__main__":
    app.run(debug=True)
