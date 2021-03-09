import numpy as np

from bin.edge_loop import EdgeLoop

class ClosedCurve(np.ndarray):
    def __init__(self):
        super.__init__(self)