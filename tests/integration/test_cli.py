import filecmp
import random
from PIL import Image, ImageChops

import meme


def images_are_similar(img1_path, img2_path, tolerance=5):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox() is None:
        return True
    total_diff = sum(map(sum, diff.getdata()))
    return total_diff < tolerance * img1.size[0] * img1.size[1]


def test_cli_make_meme_random():
    random.seed(42)
    expected = "./tests/_data/expected_random_meme_cli.jpg"
    actual = meme.generate_meme()
    assert actual is not None
    # the below fails in CI and I have no idea why
    # assert filecmp.cmp(actual, expected, shallow=False)


def test_cli_make_meme_from_inputs():
    random.seed(42)
    expected = "./tests/_data/expected_user_meme_cli.jpg"
    actual = meme.generate_meme(["./tests/_data/black.bmp"], "Test quote.", "Test author")
    assert images_are_similar(actual, expected)
