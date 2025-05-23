"""
A website that creates a colour palette based on the 10 most common colours in an uploaded image.
"""

from os import urandom
from flask import Flask, render_template, request
from file_upload_form import FileUploadForm
from utils import allowed_file, process_file


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
            img_base64, colours = process_file(file)

            return render_template(
                "index.html", form=form, image=img_base64, colours=colours
            )

    return render_template("index.html", form=form, image=image, colours=colours)


if __name__ == "__main__":
    app.run(debug=True)
