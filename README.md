# Pytest 單元測試
pytest 遵循標準的 test discovery rules，幾點要領：
- 檔名必須是符合 `test_*.py` 或 `*_test.py`
- 類別(Class)名稱必須是 `Test` 開頭，且不能有 `__init__`
- 函數與類別內的方法都必須要 `test_` 做為 prefix

## Quickstart
### 安裝 pytest 與相關會用到的套件
```shell
pip install pytest pytest-cov pytest-mock
```
### 基本 Configuration files (1)：`pytest.ini`(最常見)
> - pytest initial 時會參考的配置檔，可以在裡面設定每次 pytest 要使用的設定，通常放置於 repo 的根目錄或測試目錄中。
> - pytest 可使用的配置檔眾多，pytest.ini 文件會優先於其他文件，即使是空的。
#### 常用的配置
- `addopts`
    添加指定的 command line arguments，就好像他們是由用户指定的一樣。示例：如果你有這樣的 pytest.ini 
    ```ini=
    [pytest]
    addopts = -vv 
              --cov=src/
              --cov=api/
              --cov=script/
              --cov-report=term-missing
              --cov-config=tests/.coveragerc
    ```
    實際上就是表示使用者在 command line 下這樣的指令
    ```shell
    pytest -vv --cov=src/ --cov=api/ --cov=script/ --cov-report=term-missing --cov-config=tests/.coveragerc
    ```
    :::success
    Hint: 可以用 pytest -h 查詢可使用的 command line 選項，上述使用到的說明如下：
    - -vv:
    - --cov: 計算 coverage 的 source code 資料夾
    - --cov-report: coverage report 產出型態，term-missing 是指 print 在 terminal 上，並顯示沒寫測試（也就是 missing）的行數
    - --cov-config: 計算 coverage 的額外設定檔
    :::
- `testpaths`
    <font color=red>當 pytest command 沒有指定</font>特定目錄、文件或測試 ID 時，執行 pytest 會搜索的目錄列表(rootdir 目錄)。當所有項目測試都在一個已知的位置時很有用，以加速測試收集並避免意外地獲取不需要的測試。
    ```ini=
    [pytest]
    testpaths = tests api_tests
    ```
    這會告訴 pytest 只在 tests 和 api_tests 搜尋測試案例。
:::success
Note:
其他配置選項可以參考 [pytest.ini配置選項](https://www.osgeo.cn/pytest/reference.html#ini-options-ref)
:::

統整以上，你可能會整理出一個類似下面這樣的 `pytest.ini`
```ini=
[pytest]
addopts = -vv 
          --cov=src/
          --cov=api/
          --cov=script/
          --cov-report=term-missing
          --cov-config=tests/.coveragerc
testpaths = tests api_tests script_tests
```
### 基本 Configuration files (2)：`.coveragerc`
> 計算 coverage 的額外設定檔，可以設定計算時忽略的檔案以及不需測試的程式碼列表，可以放於根目錄或測試程式目錄並於 `pytest.ini` 指定位置
```python=
[run]
omit = 
    # omit all files in this directory
    api/*
    # omit this single file
    src/tirefire.py

[report]
exclude_lines =
    if __name__ == .__main__.:
    except ImportError:
    pass
```
## 撰寫單元測試
### 基本 function 測試範例
- 資料夾結構
<pre>
pytest_samples
├── functions
│   └── basic.py
├── functions_tests
│   ├── conftest.py
│   └── test_basic.py
├── .coveragerc
└── pytest.ini
</pre>

- `basic.py` 
```python=
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


```
- `conftest.py` : 共用的程式或 module 可以放這邊，可作用於同級與下層模塊。
```python=
import sys

sys.path.insert(0, 'functions')
```
- `test_basic.py` : 測試 `basic.py` 的程式
```python=
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

```
這時於 command line 下
```shell
pytest functions_tests/test_basic.py
```
或是
```shell
pytest
```
可以得到執行結果
![](https://i.imgur.com/POWuFMS.png)

### <font color='blue'>Class 測試</font>

### <font color='blue'>mock 的應用</font>
- 範例資料夾結構
- 先利用 sqlite 匯入測試 DB
    - Installation: 見 [連結](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm)
    - 匯入測試 DB
    ```shell
    sqlite3 testDB.db < testDB.sql
    ```
    - 看一下匯入結果(會看到一張 table cm_cust_product_code，內含 3 筆資料)
    ```shell
    sqlite3 testDB.db
    
    > select * from cm_cust_product_code;
    ```
#### Mock DB operation
- `utils.py`

#### Mock API requests




