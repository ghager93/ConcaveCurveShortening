from time import time
from time import strftime

import bin.morphology.adj_structuring_element
from bin.utils.base_dir import base_dir
from bin.tests.utils.get_test_objects import get_test_image_array
import bin.morphology as morphology

array = get_test_image_array()
structuring_element_3 = bin.morphology.adj_structuring_element.circular_structuring_element(radius=3)
structuring_element_5 = bin.morphology.adj_structuring_element.circular_structuring_element(radius=5)
structuring_element_10 = bin.morphology.adj_structuring_element.circular_structuring_element(radius=10)

output_text_path = base_dir + 'out/test_output/timer_test_output/morphology' + strftime('%Y%m%d') + '.txt'

def time_ab_function(morph_function, repeats: int = 1):
    start = time()
    for i in range(repeats):
        morph_function(array, structuring_element_3)

    return (time() - start) / repeats


def time_dilation(repeats: int = 1):
    return time_ab_function(morphology.binary_dilation, repeats)


def time_erosion(repeats: int = 1):
    return time_ab_function(morphology.binary_erosion, repeats)


def time_opening(repeats: int = 1):
    return time_ab_function(morphology.binary_opening, repeats)


def time_closing(repeats: int = 1):
    return time_ab_function(morphology.binary_closing, repeats)


def time_skeletonisation(repeats: int = 1):
    return time_ab_function(morphology.binary_skeletonisation, repeats)


def time_get_skeleton_subset(k: int, repeats: int = 1):
    return time_ab_function(morphology._get_skeleton_subset, repeats)


def time_abc_function(morph_function, k, repeats: int = 1):
    start = time()
    for i in range(repeats):
        morph_function(array, structuring_element_3, k)

    return (time() - start) / repeats


def time_get_erosions_up_to_k_times(k: int, repeats: int = 1):
    return time_abc_function(morphology._get_erosions_up_to_k_times, k, repeats)


def main():
    print('dilation:', file=open(output_text_path, 'a'))
    print(time_dilation(), file=open(output_text_path, 'a'))

    print('erosion:', file=open(output_text_path, 'a'))
    print(time_erosion(), file=open(output_text_path, 'a'))

    print('opening:', file=open(output_text_path, 'a'))
    print(time_opening(), file=open(output_text_path, 'a'))

    print('closing:', file=open(output_text_path, 'a'))
    print(time_closing(), file=open(output_text_path, 'a'))

    print('skeletonisation:', file=open(output_text_path, 'a'))
    print(time_skeletonisation(), file=open(output_text_path, 'a'))

    print('skeleton_subset, k = 1:', file=open(output_text_path, 'a'))
    print(time_get_skeleton_subset(1), file=open(output_text_path, 'a'))

    print('skeleton_subset, k = 2:', file=open(output_text_path, 'a'))
    print(time_get_skeleton_subset(2), file=open(output_text_path, 'a'))

    print('skeleton_subset, k = 3:', file=open(output_text_path, 'a'))
    print(time_get_skeleton_subset(3), file=open(output_text_path, 'a'))

    print('skeleton_subset, k = 10', file=open(output_text_path, 'a'))
    print(time_get_skeleton_subset(10), file=open(output_text_path, 'a'))

    print('erosion_k_times, k = 1', file=open(output_text_path, 'a'))
    print(time_get_erosions_up_to_k_times(1), file=open(output_text_path, 'a'))

    print('erosion_k_times, k = 2', file=open(output_text_path, 'a'))
    print(time_get_erosions_up_to_k_times(2), file=open(output_text_path, 'a'))

    print('erosion_k_times, k = 3', file=open(output_text_path, 'a'))
    print(time_get_erosions_up_to_k_times(3), file=open(output_text_path, 'a'))

    print('erosion_k_times, k = 10', file=open(output_text_path, 'a'))
    print(time_get_erosions_up_to_k_times(10), file=open(output_text_path, 'a'))


if __name__ == '__main__':
    main()
