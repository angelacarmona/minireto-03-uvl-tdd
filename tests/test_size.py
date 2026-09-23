import pytest

from catalog import classify_model_size


def test_one_feature_is_tiny():
    assert classify_model_size(1) == "tiny"

def test_zero_features_is_invalid():
    with pytest.raises(ValueError):
        classify_model_size(0)

