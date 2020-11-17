from bin.util.base_dir import base_dir
import bin.image as image
import bin.image_array as image_array

test_image_path = base_dir + 'lib/polygon_test_shapes/'


def get_test_image(filename: str = 'test1.bmp'):
    return image.open(test_image_path + filename)


def get_test_image_array(filename: str = 'test1.bmp'):
    return image_array.convert_image_to_array(get_test_image(filename))