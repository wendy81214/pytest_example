# Pytest 單元測試
pytest 遵循標準的 test discovery rules，幾點要領：
- 檔名必須是符合 `test_*.py` 或 `*_test.py`
- 類別(Class)名稱必須是 `Test` 開頭，且不能有 `__init__`
- 函數與類別內的方法都必須要 `test_` 做為 prefix

## Quickstart
### 安裝 pytest 與相關會用到的套件
```shell
pip install -r requirements.txt
```
