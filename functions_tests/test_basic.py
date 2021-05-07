"""Tests for basic.py."""
import io

import numpy as np
import pandas as pd
from pandas._testing import assert_frame_equal

from basic import add, serialize, serialize_for_recommend


def test_add():
    """Test for function add()."""
    a = 3
    b = 2
    expected_result = 5
    assert expected_result == add(a, b)


def test_for_serialize():
    """Test for function serialize()."""

    # declare a deserialize func
    def deserialize(b_str):
        parquet = io.BytesIO(bytes.fromhex(b_str))
        df = pd.read_parquet(parquet, engine='pyarrow')
        return df

    # df: test data and expected data
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                      columns=['a', 'b', 'c'])
    serialzied_result = serialize(df)
    deserialized_result = deserialize(serialzied_result)
    assert_frame_equal(deserialized_result, df)


def test_for_serialize_for_recommend():
    """Test for function serialize_for_recommend()."""
    saa_df = {'country': pd.DataFrame(),
              'industry': pd.DataFrame()}
    projection_matrix_df = {'country': pd.DataFrame(),
                            'industry': pd.DataFrame()}
    funds_varcov_df = pd.DataFrame()

    data = {
        'strategic_asset_allocation': saa_df,
        'projection_matrix': projection_matrix_df,
        'product_varcov': funds_varcov_df,
    }

    data = serialize_for_recommend(data)

    # test serialize result
    assert isinstance(data['strategic_asset_allocation']['country'], str) is True
    assert isinstance(data['strategic_asset_allocation']['industry'], str) is True
    assert isinstance(data['projection_matrix']['country'], str) is True
    assert isinstance(data['projection_matrix']['industry'], str) is True
    assert isinstance(data['product_varcov'], str) is True
