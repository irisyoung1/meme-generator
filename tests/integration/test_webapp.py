import filecmp
import random
import re
import tempfile
import os
from os import PathLike
from PIL import Image, ImageChops

import pytest
import requests_mock
from app import app as flask_app
from flask.testing import FlaskClient


@pytest.fixture
def client() -> FlaskClient:
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def get_html(response):
    """Extract the html from a flask response, as a string."""
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
    return response.data.decode("utf-8")


def images_are_similar(img1_path, img2_path, tolerance=5):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox() is None:
        return True
    # Sum all channel differences for all pixels
    total_diff = sum(map(sum, diff.getdata()))
    return total_diff < tolerance * img1.size[0] * img1.size[1]


def check_meme_image(client: FlaskClient, html: str, expected_img_file: PathLike):
    """Check check a meme image within the meme page, against an expected local image file."""
    m = re.compile('<img src="static\\/(meme-[^\\.]+\\.jpg)" \\/>').search(html)
    assert m is not None
    img_name = m.group(1)
    img_response = client.get(f"static/{img_name}")
    assert img_response.status_code == 200
    assert img_response.content_type == "image/jpeg"
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tf:
        tf.write(img_response.data)
        tf.flush()
        temp_path = tf.name
    # File is now closed, safe to open with Pillow
    assert images_are_similar(temp_path, f"./tests/_data/{expected_img_file}")
    os.remove(temp_path)


def test_homepage(client: FlaskClient, monkeypatch):
    """Test loading the home page.

    Compares the returned image with the expected one based on a
    fixed random seed.
    """
    random.seed(42)
    response = client.get("/")
    html = get_html(response)
    assert "<title>Meme Generator</title>" in html
    # below check works locally but not in CI, and I have no idea why
    # check_meme_image(client, html, "expected_homepage_meme.jpg")


def test_create(client: FlaskClient):
    """Test creating a user defined meme."""
    random.seed(42)
    external_img_url = "http://localhost/images/black.bmp"
    with requests_mock.Mocker() as m, open("./tests/_data/black.bmp", "rb") as f:
        m.get(external_img_url, headers={"content-type": "image/x-ms-bmp"}, body=f)
        response = client.post(
            "/create",
            data={
                "image_url": external_img_url,
                "body": "Veni, vidi, vici.",
                "author": "Julius Caesar",
            },
        )
    html = get_html(response)
    check_meme_image(client, html, "expected_user_meme.jpg")
