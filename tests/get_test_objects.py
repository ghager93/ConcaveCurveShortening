import bin.image as image
import bin.image_array as image_array

test_image_path = 'lib/polygon_test_shapes/test1.bmp'


def get_test_image():
    return image.open(test_image_path)


def get_test_image_array():
    return image_array.convert_image_to_array(get_test_image())