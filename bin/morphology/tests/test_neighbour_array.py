import numpy as np

from bin.morphology.util import neighbour_array
from bin.util import get_test_objects
from bin.morphology import transforms


def test_distinct_edge_array():
    sk_arr = get_test_objects.get_test_image_array('test5.bmp')

    neighbour_arr = neighbour_array.get_neighbour_array(sk_arr)
    neighbour_arr[sk_arr == 0] = 0

    distinct_edge_arr = neighbour_array._distinct_edges_vectorised(neighbour_arr)
    pass


def main():
    test_distinct_edge_array()


if __name__ == '__main__':
    main()
