# Pytest 單元測試
pytest 遵循標準的 test discovery rules，幾點要領：
- 檔名必須是符合 `test_*.py` 或 `*_test.py`
- 類別(Class)名稱必須是 `Test` 開頭，且不能有 `__init__`
- 函數與類別內的方法都必須要 `test_` 做為 prefix

## Quickstart
### 取得會用到的範例 code
```shell
git clone git@github.com:wendy81214/pytest_example.git
```
### 安裝 pytest 與相關會用到的套件
```shell
pip install -r requirements.txt
```
### 開始吧！
> 這邊提供的範例分為一般 function 測試範例(`functions/`, `functions_tests/`)、class 測試範例(`class/`, `class_tests/`)、API 測試範例(`api/`, `api_tests/`)，其實也算是模擬大家會在專案中分很多資料夾（如api, etl, batch...等等），這些所有資料夾的測試其實可以全部放在同一個資料夾裡面，但為了講解跟理解方便，我們這邊將所有測試都分開放。
- 提供的範例 code 資料夾結構
    <pre>
    pytest_example
    ├── README.md
    ├── api
    │   ├── api.py
    │   ├── driver.log
    │   ├── my_log.py
    │   ├── testDB.db
    │   ├── testDB.sql
    │   └── utils.py
    ├── api_tests
    │   ├── <font color='blue'>conftest.py</font>
    │   ├── test_api.py
    │   └── test_utils.py
    ├── functions
    │   └── basic.py
    ├── functions_tests
    │   ├── <font color='blue'>conftest.py</font>
    │   └── test_basic.py
    ├── myclass
    │   ├── Person.py
    │   ├── __init__.py
    ├── myclass_test
    │   ├── __init__.py
    │   ├── <font color='blue'>conftest.py</font>
    │   └── test_myclass.py
    ├── <font color='blue'>pytest.ini</font>
    ├── <font color='blue'>.coveragerc</font>
    └── requirements.txt
    </pre>
- 當你已經有寫好的程式需要測試時，你會需要開始新增幾個檔案如上方藍色字，這些檔案的作用會在後面詳細說明。
    - `pytest.ini`
    - `.coveragerc`
    - `conftest.py`(optional，若有測試的全域設定才會需要)
### 基本 Configuration files (1)：`pytest.ini`
> - pytest initial 時會參考的配置檔，可以在裡面設定每次 pytest 要使用的設定，通常放置於 repo 的根目錄或測試目錄中。
> - pytest 可使用的配置檔眾多，pytest.ini 文件會優先於其他文件，即使是空的。
#### 常用的配置
- `addopts`
    添加指定的 command line arguments，就好像他們是由用户指定的一樣。示例：如果你有這樣的 pytest.ini 
    ```ini
    [pytest]
    addopts = -vv 
              --cov=src/
              --cov=api/
              --cov=script/
              --cov-report=term-missing
              --cov-config=tests/.coveragerc
    ```
    實際上就是等同於使用者在 command line 下這樣的指令(所以你也可以不加在 `pytest.ini` 中，靠自己每次人工下 command --> 但很累XD)
    ```shell
    pytest -vv --cov=src/ --cov=api/ --cov=script/ --cov-report=term-missing --cov-config=tests/.coveragerc
    ```
    
    |Hint: 可以用 pytest -h 查詢可使用的 command line 選項，上述使用到的說明如下：<br> --vv: increase verbosity (印出更詳細的內容)<br> --cov: 計算 coverage 的 source code 資料夾<br> --cov-report: coverage report 產出型態，term-missing 是指 print 在 terminal 上，並顯示沒寫測試（也就是 missing）的行數<br> --cov-config: 計算 coverage 的額外設定檔<br>|
    |---|
- `testpaths`
    <font color=red>當 pytest command 沒有指定</font>特定目錄、文件或測試 ID 時，執行 pytest 會搜索的目錄列表(rootdir 目錄)。當所有項目測試都在一個已知的位置時很有用，以加速測試收集並避免意外地獲取不需要的測試。
    ```ini
    [pytest]
    testpaths = tests api_tests
    ```
    這會告訴 pytest 只在 tests 和 api_tests 搜尋測試案例。
    
|**Note**: 其他配置選項可以參考 [pytest.ini配置選項](https://www.osgeo.cn/pytest/reference.html#ini-options-ref)|
| --- |


統整以上，你可能會整理出一個類似下面這樣的 `pytest.ini`
```ini
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
```python
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
|未來在 pipeline 上 DevOps team 會幫各專案 default 加上執行 單元測試，需要麻煩大家加上 pytest.ini, .coveragerc 做設定，以利 code reviewer 協助確認測試的範圍是否合理、核心功能是否有測試到、並確認測試結果等等。|
|---|

## 來看看範例 code 並開始撰寫單元測試吧！
### <font color=#4682b4>基本 function 測試範例</font>
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
```python
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
- `conftest.py` : 共用的程式或 fixture(後面會說明fixture是什麼) 可以放這邊，可做進行全局配置，作用於同級與下層資料夾內所有測試。
```python
import sys

sys.path.insert(0, 'functions')
```
- `test_basic.py` : 測試 `basic.py` 的程式，<font color=#008080>寫測試的邏輯大致上就是:
    1. 你有一個 function 或一段程式想測試
    2. 做一些假資料
    3. 做出這些假資料經過 function 處理或程式處理後應該長怎樣(expected result)
    4. assert 假資料經過 function 處理後的 result 是否等於 expected result</font>
```python
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
![](https://storage.googleapis.com/data_questions/wendy_%E5%81%B7%E6%94%BE%E8%B3%87%E6%96%99/test_result.png)

### <font color=#4682b4>Class 測試</font>
- 範例 code: `myclass/`, `myclass_tests/`

### <font color=#4682b4>mock 的應用</font>
- 範例資料夾結構
    <pre>
    ├── api
    │   ├── api.py
    │   ├── driver.log
    │   ├── my_log.py
    │   ├── testDB.sql
    │   └── utils.py
    ├── api_tests
    │   ├── conftest.py
    │   ├── test_api.py
    │   └── test_utils.py
    </pre>
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
    ![](https://storage.googleapis.com/data_questions/wendy_%E5%81%B7%E6%94%BE%E8%B3%87%E6%96%99/db_data.png)

#### <font color=#008080>Mock DB operation</font>
> mock DB operation 的目的是希望不要在測試時不要真的對 DB 進行操作(select, insert, drop, truncate...)，這邊提供一個很簡單的範例，主要是在 DB 存取後會做一些 python 邏輯運算，我們將 DB 存取拿到的資料改成假資料(假設 sql statement 沒寫錯)，來測試後面的 python 邏輯運算是否正確。
- 範例見 `api/utils.py`, `api_tests/test_utils.py`

#### <font color=#008080>Mock API requests</font>
- 範例見: `api/api.py`, `api_tests/test_api.py`
- **Fixture**
    - 這是一個官方樣例，很明確地展示了 fixture 用法的各個細節。
    ```python
    import pytest
    import smtplib


    @pytest.fixture(scope="module")
    def smtp():
        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
        yield smtp
        smtp.close()


    def test_ehlo(smtp):
        response, msg = smtp.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
  ```
    - 首先，`@pytest.fixture` 作為裝飾器（decorator），被它作用的function即可成為一個fixture。
    - scope="module"是指定作用域。這裡的scope支持function、class、module、session四種，默認情況下的scope是function。session 則是擴大到了整個測試，可以覆蓋多個 module。
    - fixture的function名稱，可以直接作為參數，傳給需要使用它的測試樣例。在使用時，smtp並非前面定義的function，而是function的返回值，即smtplib.SMTP。這一點比較隱晦，稍微違背了Python的哲學，但卻很方便。
    - yield smtp當然也可以是return smtp，不過後面就不能再有語句。相當於只有setup、沒有teardown。使用yield，則後面的內容就是teardown。這樣不僅方便，把同一組的預備、清理寫在一起，邏輯上也更緊密。
    - 最終，在`test_ehlo`中直接聲明一個形式參數smtp，就可以使用這個fixture。同一個測試function中可以聲明多個這類形式參數，也可以混雜其它類型的參數。如果那些沒有使用smtp這個fixture的function被單獨測試，它不會被執行。
    - 另外，在fixture中，也可使用其它fixture作為形式參數，形成樹狀依賴。這為測試環境的準備，提供了更高的抽象層級。
    - 前面有提，fixture的scope中，有session，也就是整個測試過程。這意味著，fixture可以是全局的，供多個module使用。
    - 另外，pytest支持在測試的路徑下，存在<font color='blue'>`conftest.py`</font>文件，進行全局配置。
        <pre>
        tests
        ├── conftest.py
        ├── test_a.py
        ├── test_b.py
        └── sub
            ├── __init__.py
            ├── conftest.py
            ├── test_c.py
            └── test_d.py
        </pre>
        在以上目錄結構下，頂層的`conftest.py`裡的配置，可以給四個測試module使用。而 sub 下面的 `conftest.py`，只能給sub下面的兩個module使用。如果兩個 `conftest.py` 中定義了名稱相同的fixture，則可以被覆蓋； 也就是說，在sub下面的module，使用的是sub下的`conftest.py`裡的定義同名fixture。
- **Parametrizing**
   有時候，測試一個function，需要測試多種情況。而每一種情況的測試邏輯基本雷同，只是參數或環境有異。這時就需要參數化（Parametrizing）的fixture來減少重複。

    - 比如，前面smtp那個例子，可能需要準備多個郵箱來測試。
        ```python
        @pytest.fixture(params=["smtp.gmail.com", "mail.python.org"])
        def smtp(request):
            smtp = smtplib.SMTP(request.param, 587, timeout=5)
            yield smtp
            print ("finalizing %s" % smtp)
            smtp.close()
        ```
        通過在 <font color='red'>@pytest.fixture </font>中，指定參數params，就可以利用特殊對象（request）來引用request.param。使用以上帶參數的smtp的測試樣例，都會被執行兩次。

    - 還有另一種情況，直接對測試function進行參數化。
    
        ```python
        def add(a, b):
            return a + b

        @pytest.mark.parametrize("test_input, expected", [
            ([1, 1], 2),
            ([2, 2], 4),
            ([0, 1], 1),
        ])
        def test_add(test_input, expected):
            assert expected == add(test_input[0], test_input[1])
        ```
        利用<font color='red'>@pytest.mark.parametrize</font>，可以無需沒有實質意義的fixture，直接得到參數化的效果，測試多組值。

## 感謝大大回饋補充區：
- 大家可以看到我們提供的範例 code 若需要讓測試程式能夠存取到 source code，都會需要在 `conftest.py` 中加上以下 code
    ```python
    import sys

    sys.path.insert(0, 'functions')
    ```
    但其實可以利用額外的套件做到這件事情：
    - Install pytest-pythonpath
        ```shell
        pip install pytest-pythonpath==0.7.3
        ```
    - 於 `pytest.ini` 中加入 source code 的 path，以範例來說就是寫成
        ```ini
        [pytest]
        addopts = -vv 
                  --cov=functions/
                  --cov=api/
                  --cov=myclass/
                  --cov-config=.coveragerc
                  --cov-report=html:./report/coverage
                  --cov-report=term-missing
        testpaths = functions_tests api_tests myclass_test
        python_paths= functions/ api/ myclass/ 
        ```
    - 如此一來，`conftest.py` 裡面就可以清空，並且於測試程式中可以直接寫
        ```python
        from functions.basic import add, serialize, serialize_for_recommend
        ```

## References
- https://note.qidong.name/2018/01/pytest-fixture/


