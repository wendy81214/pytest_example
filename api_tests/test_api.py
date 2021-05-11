import json

import pytest
import requests

from api import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.parametrize('api_query, worker_status_code, api_status_code, api_status',
                         [({'customer_id': 1}, '1313', '200', '[Success] Finish recommend process.'),
                          ({'customer_id': 1}, '500', '500', '[Error] MLaaS internal error.'),
                          ({}, '1313', '401', '[Error] Customer ID not specified.'),
                          ({}, '500', '401', '[Error] Customer ID not specified.')])
def test_recommend_by_customer_id(mocker, app, client,
                                  api_query,
                                  worker_status_code,
                                  api_status_code,
                                  api_status):
    """
    透過 parametrize 的方式模擬『前端呼叫的各式 input 』與『第三方 API 的各式回傳結果』(也就是 requests.post 得到的第三方 API 回傳結果)，來測試自身 API 回應前端的 response 是否符合預期.

    - 這邊用到的技巧有 mock function return value, mock 第三方 API 回傳結果, 用 app.test_client()模擬打自身的 API。

    - 這邊共用到 4 個測試案例（大家可以視跟前端談定的狀況來設計，盡量羅列所有狀況）：
        1. 前端呼叫input為 {'customer_id': 1}，第三方回傳 status_code=1313，此時自身 API 回傳給前端的 json 應該為 status_code = 200, 及 msg = '[Success] Finish recommend process'
        2. 前端呼叫input為 {'customer_id': 1}，第三方回傳 status_code=500，此時自身 API 回傳給前端的 json 應該為 status_code = 500, 及 msg = '[Error] MLaaS internal error.'
        3. 前端呼叫input為 {}，第三方回傳 status_code=1313，此時自身 API 回傳給前端的 json 應該為 status_code = 401, 及 msg = '[Error] Customer ID not specified.'
        4. 前端呼叫input為 {}，第三方回傳 status_code=500，此時自身 API 回傳給前端的 json 應該為 status_code = 401, 及 msg = '[Error] Customer ID not specified.'
    """
    # === patch get_data_for_recommend() return value with empty dictionary ===
    mocker.patch('api.get_data_for_recommend', return_value=dict())

    # === patch requests.post ===
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    mocker.patch('api.requests.post',
                 return_value=MockResponse({'status_code': worker_status_code,
                                            'status': 'ok'},
                                           200))
    res = client.post('/recommend_by_customer_id', query_string=api_query)
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True))['status_code'] == api_status_code
    assert json.loads(res.get_data(as_text=True))['status'] == api_status


@pytest.mark.parametrize('api_query, worker_status_code, api_status_code, api_status',
                         [({'customer_id': 1}, '1313', '500', '[Error] MLaaS internal error.'),
                          ({'customer_id': 1}, '500', '500', '[Error] MLaaS internal error.'),
                          ({}, '1313', '401', '[Error] Customer ID not specified.'),
                          ({}, '500', '401', '[Error] Customer ID not specified.')])
def test_recommend_by_customer_id_exception(mocker, app, client,
                                            api_query,
                                            worker_status_code,
                                            api_status_code,
                                            api_status):
    """
    類似上一個測試案例，但這邊加上模擬第三方 API 出現 HTTPError 的狀況.

    - 這邊運用到 patch 的 side_effect 功能去 raise HTTPError.
    """
    # === patch get_data_for_recommend ===
    mocker.patch('api.get_data_for_recommend', return_value=dict())

    # === patch api.requests.post with HTTPError ===
    mocker.patch('api.requests.post',
                 side_effect=requests.exceptions.HTTPError())

    res = client.post('/recommend_by_customer_id', query_string=api_query)
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True))['status_code'] == api_status_code
    assert json.loads(res.get_data(as_text=True))['status'] == api_status
