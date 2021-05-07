"""Basic functions examples."""
import io

import pandas as pd


def add(a, b):
    """Add two integers."""
    return a + b


def serialize(df):
    """
    Convert dataframe to parquet string.
    @args:
        df: (DataFrame).
    @return:
        b_str: (str) Converted string.
    """
    f = io.BytesIO()
    df.to_parquet(f, engine='pyarrow')
    b_str = f.getvalue().hex()
    return b_str


def serialize_for_recommend(data):
    """
    Convert all keys that value is dataframe to parquet string.
    @args:
        data: (dict) Data for recommendation .
    @return:
        data: (dict) Some value converted to parquet string.
    """
    data['strategic_asset_allocation']['country'] = \
        serialize(data['strategic_asset_allocation']['country'])
    data['strategic_asset_allocation']['industry'] = \
        serialize(data['strategic_asset_allocation']['industry'])
    data['projection_matrix']['country'] = \
        serialize(data['projection_matrix']['country'])
    data['projection_matrix']['industry'] = \
        serialize(data['projection_matrix']['industry'])
    data['product_varcov'] = serialize(data['product_varcov'])
    return data


if __name__ == '__main__':
    pass
