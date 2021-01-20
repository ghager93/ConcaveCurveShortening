from unittest import TestCase
import numpy as np

import bin.morphology as morphology
import bin.adj_image_array as image_array


class Test(TestCase):
    def test__zs_calculate_neighbour_array(self):
        a = np.array([[1, 0, 0], [0, 1, 1], [0, 0, 0]])

        assert np.array_equal(morphology._zs_calculate_neighbour_array(a),
                              np.array([[8, 88, 48], [5, 132, 64], [2, 3, 129]]))
