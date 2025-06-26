"""Web app module."""
import mimetypes
import os
import random
import tempfile
from pathlib import Path

import requests
from MemeGenerator.engine import MemeEngine
from QuoteEngine.ingestor import Ingestor
from flask import Flask, render_template, request

app = Flask(__name__)
current_dir = Path(__file__).parent
meme = MemeEngine(current_dir / "static")


def setup():
    """Load all resources."""
    Ingestor.register_defaults()
    return Ingestor.scan(current_dir / "_data/DogQuotes"), MemeEngine.find_images(
        current_dir / "_data/photos/dog/"
    )


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme."""
    img, quote = (random.choice(item) for item in (imgs, quotes))
    meme_path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=Path(meme_path).relative_to(current_dir))


@app.route("/create", methods=["GET"])
def meme_form():
    """Accept user input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form.get("image_url")
    body = request.form.get("body")
    author = request.form.get("author")

    response = requests.get(image_url, allow_redirects=True)
    content_type = response.headers["content-type"]
    extension = mimetypes.guess_extension(content_type)
    # Accept BMP images as well
    if not extension and content_type == "image/x-ms-bmp":
        extension = ".bmp"
    if not extension:
        raise ValueError(
            f"Unsupported content type: {content_type} for {image_url} (is it an image?)"
        )
    tf = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
    try:
        tf.write(response.content)
        tf.close()  # Close so Pillow can open it on Windows
        meme_path = meme.make_meme(tf.name, body, author)
    finally:
        os.remove(tf.name)
    # Always pass a web path for the static file
    return render_template("meme.html", path=f"static/{Path(meme_path).name}")


if __name__ == "__main__":
    app.run()
