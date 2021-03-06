from unittest.mock import Mock

import pytest

from utils import get_data_for_recommend


@pytest.mark.parametrize('customer_id, fetchone_result, data',
                         [('1', ('BNDF',), {'id': '1', 'product_codes': 'BNDF', 'cust_type': '00'}),
                          ('2', ('ETFF',), {'id': '2', 'product_codes': 'ETFF', 'cust_type': '01'}),
                          ('3', ('STKF',), {'id': '3', 'product_codes': 'STKF', 'cust_type': '01'})])
def test_get_data_for_recommend(mocker, customer_id, fetchone_result, data):
    """
    透過 paratetrize 模擬 mock cursor.fetchone() 的三種結果來測試後續 python 邏輯是否正確.

    - 這邊需要 mock get_conn()、並實作 class MockConn, MockCursor 來模擬 connection, cursor
    - 這邊會稍微麻煩一點，因為用 with get_conn() as conn: 的寫法，會需要實作 __enter__, __exit__ 兩個 metho
    """
    class MockCursor:
        def __init__(self, fetchone_result):
            self.fetchone_result = fetchone_result

        def execute(self, sql_statement):
            pass

        def fetchone(self):
            return self.fetchone_result

    class MockConn:
        def __init__(self, cursor_obj):
            self.cursor_obj = cursor_obj

        def cursor(self):
            return self.cursor_obj

        def close(self):
            pass

    logger = Mock()

    # mock get_conn() and cursor
    mock_conn = Mock()
    mock_conn.__enter__ = Mock(return_value=MockConn(MockCursor(fetchone_result)))
    mock_conn.__exit__ = Mock(return_value=None)
    mocker.patch('utils.get_conn', return_value=mock_conn)

    result = get_data_for_recommend(customer_id, logger)
    assert data == result
