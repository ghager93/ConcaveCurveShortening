from unittest import TestCase

from bin.image_array import *
from bin.utils.base_dir import base_dir
from bin.utils.imshow import show


class Test(TestCase):
    test_belize_image_path = base_dir + '/lib/silhouettes/belize-silhouette.bmp'
    test_belize_image = Image.open(test_belize_image_path)
    test_array = np.arange(16).reshape((4, 4)) % 3

    def test_convert_image_to_array(self):
        array = convert_image_to_array(self.test_belize_image)
        pass

    def test_convert_image_to_binary_array(self):
        bin_array = convert_image_to_binary_array(self.test_belize_image)
        pass

    def test_convert_to_image(self):
        image = convert_to_image(self.test_array)
        pass

    def test_convert_to_points_list(self):
        points_list = convert_to_points_list(self.test_array)

    def test_boolean_sum(self):
        assert boolean_sum(self.test_array) == 10

    def test_boolean_ratio(self):
        test_array2 = np.arange(16).reshape((4,4)) % 2
        assert boolean_ratio(self.test_array, test_array2) == 10 / 8

    def test_is_boolean_subset_of_false(self):
        test_array2 = np.arange(16).reshape((4, 4)) % 2
        assert not is_boolean_subset_of(test_array2, self.test_array)

    # def test_is_boolean_subset_of_true(self):
    #     test_array2 = np.arange(16).reshape((4, 4)) % 3
    #     test_array2[0, :] = 0
    #     assert is_boolean_subset_of(test_array2, self.test_array)

    def test_pad_by_zeroes(self):
        assert pad_by_zeroes(self.test_array).shape == (6, 6)

    def test_pad_by_ones(self):
        assert pad_by_ones(self.test_array).shape == (6, 6)

    def test_invert(self):
        inverse_test_array = np.array([[1, 0, 0, 1],
                                       [0, 0, 1, 0],
                                       [0, 1, 0, 0],
                                       [1, 0, 0, 1]])
        assert np.array_equal(invert(self.test_array), inverse_test_array)

    def test_show(self):
        show(self.test_array, close_method=CLOSE_METHOD_TIMER, close_time=1)
