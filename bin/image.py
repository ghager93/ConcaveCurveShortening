from PIL import Image
from PIL import ImageOps


def open(path: str):
    try:
        return Image.open(path)
    except:
        print('Unable to open image at path', path)


def open_as_binary(path: str):
    return _convert_to_binary(open(path))


def _convert_to_binary(image: Image.Image):
    return image.convert('1')


def resize_by_absolute_dimensions(image: Image.Image, new_dimensions: list):
    _assert_resize_parameters(new_dimensions)
    return image.resize(new_dimensions)


def resize_by_percentage(image: Image.Image, resize_percentage: list):
    _assert_resize_parameters(resize_percentage)
    return image.resize((int(resize_percentage[0]*image.width), int(resize_percentage[1]*image.height)))


def _assert_resize_parameters(dimensions: list):
    assert len(dimensions) == 2
    assert dimensions[0] > 0 and dimensions[1] > 0


def scale(image: Image.Image, scale: float):
    assert scale > 0
    return ImageOps.scale(image, scale)


def pad_by_zeroes(image: Image.Image, pad_width: int):
    _assert_pad_parameters(pad_width)
    return ImageOps.expand(image, pad_width)


def _assert_pad_parameters(pad_width):
    assert pad_width > 0


def save(image: Image.Image, path: str):
    image.save(path)