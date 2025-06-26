import random
from tempfile import TemporaryDirectory
from PIL import Image, ImageChops

from MemeGenerator.engine import MemeEngine


def images_are_similar(img1_path, img2_path, tolerance=5):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox() is None:
        return True
    total_diff = sum(map(sum, diff.getdata()))
    return total_diff < tolerance * img1.size[0] * img1.size[1]


def test_make_meme():
    random.seed(42)
    expected = "./tests/_data/expected_make_meme.jpg"
    with TemporaryDirectory() as d:
        me = MemeEngine(d)
        actual = me.make_meme("./tests/_data/black.bmp", "Test quote.", "Test author")
        assert images_are_similar(actual, expected)
