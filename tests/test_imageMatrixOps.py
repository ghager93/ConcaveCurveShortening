from unittest import TestCase
from old import segmenting


class TestImageMatrixOps(TestCase):
    im = segmenting.getTestImageMatrix()

    def test_xor_edge_detect2(self):
        im_xor2 = self.im.xorEdgeDetect2()
