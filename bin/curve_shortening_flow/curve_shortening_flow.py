import numpy as np

from . import _masking
from . import _point_spread
from . import vector_diff
from . import metrics

from bin.edge_loop import EdgeLoop


class CurveShorteningFlow():
    MAX_ITER = 5000

    def __init__(self, sigma_n=1, sigma_u=1):
        self._mask_f = _masking.continuous_heaviside_non_negative_f()
        self._normal_spread_f = _point_spread.gaussian_func(sigma_n)
        self._update_spread_f = _point_spread.gaussian_func(sigma_u)
        self._step_size = 1
        self._step_size_update_factor = 2
        self._downsample_factor = 2
        self._concavities = []

    def run(self, x):
        out = []
        for i in range(self.MAX_ITER):
            out.append(x)
            x = self._update(x)

            if self._break_condition(x):
                break

        return out

    def _step(self, n_spread, tangent):
        return self._update_spread_f(self._mask_f(np.cross(n_spread, tangent))[:, None] * n_spread)

    def _concavity(self, n_spread, tangent):
        return sum(self._mask_f(-np.cross(n_spread, tangent)))

    def _update(self, x):
        n_spread = self._normal_spread_f(vector_diff.normal(x))
        tangent = vector_diff.tangent(x)

        self._concavities.append(self._concavity(n_spread, tangent))

        if(self._concavities[-1] <= 0):
            return x

        self._step_size_update(x)
        x = self._downsample(x)
        x = self._discretise(x)

        n_spread = self._normal_spread_f(vector_diff.normal(x))
        tangent = vector_diff.tangent(x)

        return x + self._step_size * self._step(n_spread, tangent)

    def _step_size_update(self, x):
        if self._step_size_update_condition(x):
            self._step_size *= 2

    def _step_size_update_condition(self, x):
        return abs(self._dconcavities()) < 0.1

    def _downsample(self, x):
        if self._downsample_condition(x):
            return x[::self._downsample_factor]
        return x

    def _downsample_condition(self, x):
        return abs(self._dconcavities()) < 0.1

    def _discretise(self, x):
        if self._discretise_condition(x):
            _, idx = np.unique(np.around(x), axis=0, return_index=True)
            return x[np.sort(idx)]
        return x

    def _discretise_condition(self, x):
        return False

    def _dconcavities(self):
        if len(self._concavities) > 1:
            return self._concavities[-1] - self._concavities[-2]
        return np.inf

    def _break_condition(self, x):
        return self._concavities[-1] <= 0
