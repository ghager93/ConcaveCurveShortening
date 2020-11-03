from unittest import TestCase
from PIL import ImageOps

from bin.image_array_ops import *
from bin.image_array import *
from bin.image import *
from bin.util.base_dir import base_dir


class Test(TestCase):
    test_belize_image_path = base_dir + '/lib/silhouettes/belize-silhouette.bmp'
    test_belize_image = resize_by_percentage(Image.open(test_belize_image_path).convert('L'), (0.1, 0.1))
    test_belize_array = invert(convert_image_to_array(test_belize_image))

    def test_smooth(self):
        smoothed_array = smooth(self.test_belize_array, 5)
        show(self.test_belize_array, close_method=CLOSE_METHOD_TIMER, close_time=1)
        show(smoothed_array, close_method=CLOSE_METHOD_TIMER, close_time=1)

    def test_edge_detect(self):
        self.fail()

    def test__xor_edge_detect(self):
        self.fail()

    def test_find_polygons(self):
        self.fail()
