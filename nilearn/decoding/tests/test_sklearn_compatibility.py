import numpy as np
from ..space_net import (TVl1Classifier, TVl1Regressor,
                         SmoothLassoClassifier, SmoothLassoRegressor)
from nose.tools import assert_true
import traceback


def test_get_params():
    # Issue #12 (on github) reported that our objects
    # get_params() methods returned empty dicts.

    cv_addition_params = ["n_alphas", "eps", "cv", "alpha_min"]
    for model in [SmoothLassoClassifier, TVl1Classifier,
                  TVl1Regressor, SmoothLassoRegressor]:
        kwargs = {}
        if model.__name__.endswith('CV'):
            kwargs['alphas'] = np.logspace(-3, 1, num=5)
        for param in ["max_iter", "alpha", "l1_ratio", "verbose",
                      "tol", "mask", "memory", "copy_data",
                      "fit_intercept", "alphas"] + [
            [], cv_addition_params][model.__name__.endswith("CV")]:
            if model.__name__.endswith("CV"):
                if param == "alpha":
                    continue
            elif param == "alphas":
                continue

            m = model(**kwargs)

            try:
                params = m.get_params()
            except AttributeError:
                if "get_params" in traceback.format_exc():
                    params = m._get_params()
                else:
                    raise

            assert_true(param in params,
                        msg="Class '%s' doesn't have parameter '%s'." % (
                    model.__name__, param))
