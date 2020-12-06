from bin.util.base_dir import base_dir
import bin.image as image
import bin.image_array as image_array
import bin.image_array_ops as image_array_ops

test_image_path = base_dir + 'lib/polygon_test_shapes/'
country_path = base_dir + 'lib/silhouettes/'
skeleton_path = base_dir + 'lib/skeletons/'


def get_test_image(filename: str = 'test1.bmp'):
    return image.open_image(test_image_path + filename)


def get_test_image_array(filename: str = 'test1.bmp'):
    return image_array.convert_image_to_array(get_test_image(filename))


def get_smoothed_country_array(filename: str = 'afghanistan-silhouette.bmp'):
    im = image.open_image(country_path + filename)
    im = image.resize_by_percentage(im, (0.25, 0.25))
    array = image_array.convert_image_to_array(im)
    array = image_array.invert(array)
    array = image_array_ops.smooth(array, 5)

    return array


def get_country_skeleton_array(filename: str = 'afghanistan.bmp'):
    return image_array.convert_image_to_array(image.open_image(skeleton_path + filename))
