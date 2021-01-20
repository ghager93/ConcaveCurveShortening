import numpy as np

import bin.skeleton.skeleton_ops
from .msp import decimate

from bin.msp.upsample import upsample

from .utils.image import convert_to_points_list, point_map_to_image

from .morphology import transforms

from bin.skeleton.skeleton_ops import image_root, skeleton_to_root_distance_map, skeleton_tree_query


def morphological_distance_image(image, ratio=0.1):
    decimated_image = decimate.decimate(image, ratio)
    decimated_image_points = convert_to_points_list(decimated_image)

    skeleton = transforms.skeleton_transform(image)
    skeleton_points = convert_to_points_list(skeleton)

    body_to_skeleton_distances, body_to_skeleton_pairs = skeleton_tree_query(decimated_image_points, skeleton_points)

    body_to_skeleton_distance_image = point_map_to_image(dict(zip(decimated_image_points, body_to_skeleton_distances)),
                                                         image.shape)
    downsized_b2s_distance_image = decimate.downsize(body_to_skeleton_distance_image, ratio)

    skeleton_to_root_distance_map_ = skeleton_to_root_distance_map(image_root(image, skeleton), skeleton)
    body_mapped_s2r_image = point_map_to_image(
        dict(zip(decimated_image_points,
                 [skeleton_to_root_distance_map_[skeleton_points[p]] for p in body_to_skeleton_pairs])),
        image.shape
    )
    downsized_body_mapped_s2r_image = decimate.downsize(body_mapped_s2r_image, ratio)

    downsized_morph_image = downsized_b2s_distance_image + downsized_body_mapped_s2r_image
    downsized_morph_image_inverted = np.where(downsized_morph_image != 0, 1 / downsized_morph_image, 0)
    morph_image_inverted = upsample(downsized_morph_image_inverted, image.shape, ratio)
    morph_image = np.where(morph_image_inverted != 0, 1 / morph_image_inverted, 0)

    return morph_image
