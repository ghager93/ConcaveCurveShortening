import numpy as np

from . import skeleton_ops
from . import transforms
from . import bones


class SkeletonGraph:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.skeleton = transforms.skeleton_transform(image)
        self.nodes = skeleton_ops.nodes(self.skeleton)
        self.edges = skeleton_ops.distinct_edges(self.skeleton)
        self.ends = skeleton_ops.end_points(self.skeleton)
        self.branches = skeleton_ops.branch_points(self.skeleton)
        self.root = skeleton_ops.image_root(self.image, self.skeleton)
        self.joint_graph = bones.JointGraph(self.joints(), bones.bones(self))

    def joints(self):
        return self.ends | self.branches | {self.root}

    def joints_array(self):
        out = np.zeros(self.skeleton.shape, int)
        out[tuple([x for x in zip(*self.joints())])] = 1
        return out
